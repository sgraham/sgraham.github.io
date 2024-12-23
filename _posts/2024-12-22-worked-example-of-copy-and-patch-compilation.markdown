---
layout: newpost
title: A worked example of copy-and-patch compilation
---

I've been working on-and-off on a toy compiler. It started when I
thought it would be a good idea to add [extra language
features](https://scot.tg/2023/11/06/more-questionable-c-compiler-ideas/)
to the C compiler I was working on. I eventually decided that was
probably a poor idea, but that writing a completely new language made
sense (?). Or was at least more fun!

In any case, I have been grappling on-and-off with that enjoyable black
hole of a project, but it's still deep in the "not working yet" phase.

Along the way [I had a
vision](https://scot.tg/2024/12/20/60-fps-compiler/) that I'm sure is
oft-repeated in various forms by other old people:

> "My Turbo Pascal projects [compiled in, like, a second](https://youtu.be/E6TxE8dQOIA?si=G8sRJv5lByNgSvzL&t=990)",

and were running on a computer (charitably, let's say a `486DX33`) that
ran at 33MHz, whereas the computer I'm sitting at now runs at 3.8GHz.
That's _at least_ 100 times faster, and that's before we even consider
the fact that the modern one has **24** cores vs. the old one having
exactly **one**!

And yet somehow, I'm able to read most of reddit/lobste.rs/this blog
post while waiting for my C++/Rust/whatever to compile and link. Are
today's projects bigger? Sure, of course. Are they so much bigger and
badly designed that we need to throw away something like a ~2400x
difference in performance?

So! With that motivational speech in my mind, I checked my own toy
compiler and found it, not surprisingly, disappointingly slow[^1].

I started investigating a bunch of restructuring ideas, but codegen was
the biggest piece of the pie, and also seems to be most variable
time-wise. The [copy-and-patch](https://arxiv.org/pdf/2011.13127) paper
from 2021 was a neat twist on other older snippet-like approaches. And
when you read the paper it sounds relatively straightforward, other than
a few details like how you actually perform some of the transformations,
how registers are allocated and tracked etc. There is an [associated
code repository](https://github.com/sillycross/PochiVM), but I found the
essential details are very obscured[^2] by
[piles](https://github.com/sillycross/PochiVM/blob/master/pochivm/arith_expr_fastinterp.cpp)
[of](https://github.com/sillycross/PochiVM/blob/master/pochivm/ast_catch_throw_fastinterp.cpp)
[repetitive](https://github.com/sillycross/PochiVM/blob/master/pochivm/cast_expr_fastinterp.cpp)
[code](https://github.com/sillycross/PochiVM/blob/master/pochivm/function_proto_fastinterp.cpp),
and the extensive (excessive?) C++ template metaprogramming employed for
the application they've chosen to apply the technique to.

In the interests of clarifying it in my **own** mind (and for future me
who will likely forget how it works in a few months), I thought I'd make
a standalone example of the technique, and note some things that seemed
subtle.

## Copy-and-patch compilation

The high-level idea is to use `clang -O3` to generate little snippets
(called "stencils" in the paper) of code that can be matched to your
compiler's AST/bytecode/whatever. There's two important tricks in this
part. The first is that we want reliable holes in the stencils so that
we can fill them at (our) compile time with the values we want.

This could be achieved by compiling, e.g:
```c
extern int get_value_0();
extern int get_value_1();
int do_add(void) {
    int lhs = get_value_0();
    int rhs = get_value_1();
    return lhs + rhs;
}
```
But this would generally suck, as if you stitch together a whole bunch
of these, you'd be `push`, `pop`, `call`ing constantly (as would be very
common in a naive bytecode JIT).

So the first trick is instead to compile:

```c
extern uintptr_t K0;
extern uintptr_t K1;
int do_add(void) {
    return (int)&K0 + (int)&K1;
}
```

Then, if you parse the object file, because the variables are `extern`
the compiler necessarily has to generate two relocation records (for
`K0` and `K1`) for the linker to fix up. Instead of replacing them with
**addresses** when we rip the code out of the object file, we instead
replace them with the **actual values** we want to add.

This is a bit better, but the second trick makes it even better. Instead
of performing an operation in a normal function-type way and returning
the result, we change the stencils in two ways. The first is to change
the calling convention to the
[GHC](https://llvm.org/docs/LangRef.html#calling-conventions) one. This
very unusual calling convention has _no_ callee save registers. The
second change is to make every function take a continuation and tail
call it (so it doesn't _need_ to save any registers).

So what does that all mean? The "add" function would now look like:

```c
extern uintptr_t CONT;
void __ghccc do_add(int a, int b) {
    int v = a + b;
    [[musttail]] return ((void(*__ghccc)(void))&CONT)(v);
}
```
That is, it takes two arguments, and then instead of returning the
result, calls to a provided (patchable) address, putting the result in
the first call parameter slot.

Because of the calling convention of passing everything in registers,
`a` and `b` will be whatever the first two are (happens to be `r13` and
`rbp`), and then `v` will be in turn passed to the continuation in
`r13`. The cool part is that as long as the order is maintained when
passing other arguments, there's no shuffling of registers, so the
arguments to the function are effectively the "registers in use".

As long as the `[[musttail]]`-blah-blah has all the right calling
convention goop, it will compile to a `jmp $+0` (where we're writing the
offset), so in practice it's just:

```asm
do_add:
    add rbp, r13
    jmp <somewhere>
```

And because we know that we're going to put the next continuation right
after this one to use the result of the `do_add`, we can just drop the
`jmp` entirely if there's not any conditional branching happening.

The only thing you have to do then, is "preserve" the pending
computation results in values as they get passed from continuation to
continuation. What this looks like in practice is keeping track of how
many values are on the virtual stack, and including them before your
arguments in the continuation that you use. So if there were already two
other values, you'd instead use:

```c
extern uintptr_t CONT;
void __ghccc do_add_with_2(uintptr_t r0, uintptr_t r1, int a, int b) {
    int v = a + b;
    [[musttail]] return ((void(*__ghccc)(uintptr_t, uintptr_t))&CONT)(r0, r1, v);
}
```

By passing `r0, r1` in, and then passing them on to the continuation in
the same call location, they will be instead be in `r13` and `rbp`, and
our addition computation of `a`, `b`, and `v`, will be in the next
registers `r12` and `rbx` instead. So the generated code is identical,
except with different register allocations:

```asm
do_add_with_2:
    add r12, rbx
    jmp <somewhere>
```

## An actual in-the-details example

Did you get all that? Me neither at first, so I hacked up a [standalone
example](https://github.com/sgraham/copy-n-patch) of both the build time
and the run time.

The example is attempting to apply this technique to evaluating `a = (b + c + f * g) * (d + 3)`.
It does a (fake) tokenization, then a (fake)
parse, and then pretends to walk the parse tree to generate code by
calling stencil functions.

The PochiVM paper code goes to great lengths to embed LLVM, build the
AST using C++ metaprogramming, constexpr to burn things in, etc.

I just did what I always do and use Python to hack something together
`:-p`. It templates some C code, patches the intermediate .ll files, then
rips the code and reloctions out of the obj file to generate  _another_
set of C functions. This second set of C functions are linked into the
compiler you're actually writing, and are basically like `memcpy` with
some holes. That is, you pass in the constants and addresses that you
want burned in, and it blasts out the code that does the `add` (or
whatever more complex operation was generated in the stencil).

### Generating snippets/stencils

The generator is
[clang_rip.py](https://github.com/sgraham/copy-n-patch/blob/main/clang_rip.py). Taking our running example of adding, the template code looks like:

```python
for ir in range(4):
    with CToObj("add", ir, sf) as c:
        c.build_decl(["int a", "int b"])
        c.emit("{ int v = a + b;")
        c.build_continuation(0, ["v"])
        c.emit("}")
```
That just generates a function that looks like the `do_add`s above, but
for multiple copies (`range(4)`) that add various "saved registers". It
compiles each of those functions by itself into an obj file, reads the
`.text` and relocations, then writes an entry to `snippets.c` that does
the aforementioned `memcpy`-ish thing to generate. In the case of `add`,
there's no required constants (it's assuming both values are in
registers), so the only relocation would be the one for where the
continuation is going.

One subtle bit (x64-specific I guess, but other targets likely have
similar restrictions) is that clang reasonably assumes that the
addresses of all code and references are going to be with 2G of the
instruction pointer (this is how all code is compiled by default). But
because we're using the `extern uintptr_t`s as arbitrary values to burn
in, we might want an offset or value that's larger than 2^31 away. By
using the `-mcmodel=medium` or `-mcmodel=large` we can tell clang that
we don't want to make this assumption. That is, that it should allow a
full 8 byte address when loading the value of the variable. This causes
it to use the more expensive sequence:
```
movabs rax, 0x0000000000000000
mov rNN, rax
```
in those cases. But by using this flag only for some choice snippets
(i.e. `uint64_t` const loading) the lack of range problem can be
avoided, without making all the rest of the code less efficient.

Another unfortunate subtlety is that you can't actually tell clang in C
code to use the GHC calling convention. So instead, when generating
snippets in C we use the (also uncommon, but has a keyword)
`__vectorcall` calling convention. This gives us a nice simple/dumb
keyword to replace in the LLVM IR with the annotations that specifies
`ghccc` before having clang generate the final target object file.

Similarly, the `[[musttail]]` attribute can't be applied properly in the
source C, so we do that in the `.ll` file too.

### Using the stencils

After doing our pretend lex/parse, we have a parse tree that looks like
this for our target expression `a = (b + c + f * g) * (d + 3)`:

```
          =
         / \
        a   *
           / \
          /   \
         +     +
        / \   / \
       /   \ d   3
      +     *
     / \   / \
    b   c f   g
```
and when flattened into an array representing a post-order[^3] walk we
have this:

```
00: NAME (lval) 'a'
01: NAME 'b'
02: NAME 'c'
03: ADD
04: NAME 'f'
05: NAME 'g'
06: MUL
07: ADD
08: NAME 'd'
09: CONST 3
10: ADD
11: MUL
12: ASSIGN
```

Then, the code to actually do the copy-and-patch compilation using the
snippets we generated looks like this:

```c
load_addr_0("a")    //  0 NAME (lval) 'a'    vstack now [&a             ]
load_1("b")         //  1 NAME 'b'           vstack now [b &a           ]
load_2("c")         //  2 NAME 'c'           vstack now [c b &a         ]
```

Again, the `_0`, `_1`, `_2` suffixes are telling the generator how many
registers to pass through untouched, and is calculated by **the number
of values on the vstack before the call, not including arguments this
function is actually taking**. So, continuing on down the parse tree,
`add` is going to consume two of the vstack values ("b" and "c") and
wants to keep one ("&a"), so it uses the `_1` variant of `add`.

```c
add_1()             //  3 ADD                vstack now [r0 &a          ]
```

r0 here represents the result of the add for which there's no name. It
has a register assigned, but it wouldn't be the first register, that
would be `&a`.

```c
load_2("f")         //  4 NAME 'f'           vstack now [f r0 &a        ]
load_3("g")         //  5 NAME 'g'           vstack now [g f r0 &a      ]
mul_2()             //  6 MUL                vstack now [r1 r0 &a       ]
add_1()             //  7 ADD                vstack now [r2 &a          ]
load_2()            //  8 NAME 'd'           vstack now [d r2 &a        ]
const_3(3)          //  9 CONST 3            vstack now [3 d r2 &a      ]
```
Slightly badly chosen example data, `const_3(3)` is **both** loading the
constant "3" for computation, and also `_3` passing through 3 untouched
registers (for "d", "r2", and "&a"). Finishing up:

```c
add_2()             // 10 ADD                vstack now [r3 r2 &a       ]
mul_1()             // 11 MUL                vstack now [r4 &a          ]
assign_indirect_0() // 12 ASSIGN             vstack now [               ]
```

And we're done!

### Generated code

Now that was a lot of futzing around, and you might be thinking "why
bother?", it's a pile of preprocessing when I could just bang out some
asm and encode some instructions myself. The upsides are:
- well-optimized `clang -O3` local code, with the side benefit of clang
  dealing with all the instruction encoding junk
- pretty good register allocation (greedy, but much better that a
  typical push/pop heavy JIT)
- good control flow without unnecessary/non-branch-predictable jumps
  and calls.

One thing that I'm a little uncertain on after implementing this and
referring back to the paper is that they mention doing register
allocation and the C++ metaprogramming goes to a lot of bother to
permute out versions that require stack spills. I'm a little unclear if
I just don't understand when this would be required, or if it's no
longer required because of improvements in clang's implementation of the
`ghccc` calling convention. As far as I can tell, you can pass as many
arguments as you want.

It will get less efficient, of course, if there's no registers left for
temporaries because then clang will have to spill and restore, but as
long as it keeps all, say, 30 arguments from the _input_ to the
function, and gets them in the same order/location in the _invocation_
of the continuation, I don't see why we would have to do anything else.

There were some mentions of `ghccc` only supporting 10 integer arguments
which would mean only 10 live values on the virtual stack, but as far as
I can tell from testing, it seems to stash the rest of them relative to
`rsp` and then shuffle as necessary in the body of the function. (Please
let me know if you happen to more/better about this!)

Anyway, here's the full disassembly of the generated code from the
example when run:

```
00000145DBFA0000  lea         rbp,[145DBFB0000h]              ; load &a
00000145DBFA0007  mov         r12d,dword ptr [145DBFB0004h]   ; load b
00000145DBFA000E  mov         ebx,dword ptr [145DBFB0008h]    ; load c
00000145DBFA0014  add         r12d,ebx                        ; b+c
00000145DBFA0017  mov         ebx,dword ptr [145DBFB0014h]    ; load f
00000145DBFA001D  mov         r14d,dword ptr [145DBFB0018h]   ; load g
00000145DBFA0024  imul        ebx,r14d                        ; f*g
00000145DBFA0028  add         r12d,ebx                        ; b+c + f*g
00000145DBFA002B  mov         ebx,dword ptr [145DBFB000Ch]    ; load d
00000145DBFA0031  mov         r14,3                           ; const 3
00000145DBFA003B  add         ebx,r14d                        ; d+3
00000145DBFA003E  imul        r12d,ebx                        ; (b+c + f*g) * (d+3)
00000145DBFA0042  mov         dword ptr [rbp],r12d            ; store into &a
```

It's basically a straight translation of the operations we wanted, using
registers pretty effectively, and with no unnecessary branching or
indirection. I feel this would produce very competitive to `-O0` (or
even `-O1` code in some cases), and in practice I think it'd be
extremely fast to do so.

In this setup, I've made the parse tree nodes, and the stencils very
tiny low-level operations, almost like bytecode, but there's nothing
that restricts you to that.

You could imagine in theory you could have a stencil that happens to
calculate `(A+B + C*D) * (E+3)` which almost fully matches our
"program". In that case clang would have been run at `-O3` on the full
structure of the program so it would be able apply whatever fancy
optimizations it could to the whole expression. More reasonably though,
it seems to make sense to have larger nodes that say, "check a
conditional and run either a then block or an else block", etc. which
would match and handle a larger chunk of the parse tree.

I'm not quite sure how to set up and structure that pattern matching
yet, but I think it's probably similar to something like "finding the
longest matching string" so I'm sure someone found the optimal way to do
it sometime before 1980.

### Clear as mud

That was a quite a lot of typing. But hey, maybe your C++/Rust build is
finally done!

I'm not sure if it actually communicated much to anyone other than me
either, but maybe stepping through the example code will be useful too
if you're trying to figure it out how this works. Or get in touch, it's
fun stuff to talk about!

---
[^1]: It also doesn't work, so whether it's fast to compile is not overly important!

[^2]: This could certainly be my lack of knowledge/patience for reading such code, another more patient reader might be able to get a lot more out of that repo!

[^3]: If you can never remember what that name is supposed to mean like I cannot, "post-order" means visit children (leaves), then visit the parent, typically visiting the children from left-to-right (but any fixed order would be fine I guess).
