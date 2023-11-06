---
layout: newpost
title: More questionable C compiler ideas
---

After my [pdb detour](/2023/05/02/debugging-with-pdbs/), I used the
"[prototype IDE](https://www.youtube.com/watch?v=Di-GK1RkYh8)" for a
while to hack up a little platformer.

Not-even-saving-the-file code updates are definitely the way to go! It's
very fun when you can just type things and see them pop up
**immediately** after the keystroke that types the last letter.

### Crashy and fuzzy

I quickly discovered a variety of ways to crash the compiler
(oops![^1]), so I spent a while fixing all of those that I encountered.
This made the editor/compiler/runtime combo stable enough that I could
type random C for an hour or so without crashing everything.

I also added a [fuzzer
target](https://github.com/sgraham/dyibicc/blob/main/src/fuzz_entry.c)
hoping to further improve stability. It's just a simple integration for
[libFuzzer](https://llvm.org/docs/LibFuzzer.html) (aka
`-fsanitize=fuzzer` in clang) and it passes the fuzz input directly to
the compiler update function. This found some bugs in the tokenizer and
preprocessor so it was kind of a success.

But unfortunately, even with a helper corpus I only managed to find a
couple parser bugs, and no codegen bugs. It is **highly** improbable
that the reason I didn't find more parser and codegen bugs because they
don't exist. Rather, the problem is that the fuzzer is unable to
generate valid-enough semi-C-shaped inputs to make it to those
codepaths.

I did a little hunting around for fuzzers that specialize in fuzzing
compilers. It looks like some people have tried, but nothing too great,
and I didn't have much success integrating them, so better fuzzing will
have to wait for now. (Suggestions?)

### More ways to crash

This is of course a C compiler, and C compilers compile C code, and C
code is eminently capable of writing its own crashes too!

So once the compiler wasn't crashing, my next source of
[flow](https://en.wikipedia.org/wiki/Mihaly_Csikszentmihalyi#Flow)-interruption
is when I write game code that dereferences null or reads out of bounds
or whatever.

I haven't tried to work on this problem yet, but I think that will be
the next thing to do in the game shell. It should be possible to add
some amount of sandboxing to the game's C code so that it runs normally
in-process, but can trap (say) access violations at the shell level and
report a user error, while maintaining a functioning compiler REPL, so
that the error can be repaired without restarting.

### Easier embedding

When embedding the compiler into another program, `libdyibicc.c` and
`.h` were required of course, but in addition, you also had to have a
copy of (and point the compiler at) the compiler's [built-in include
directory](https://github.com/sgraham/dyibicc/tree/main/include). This
didn't really spark joy because it gets into file system path
manipulation, non-obvious initial setup steps, etc.

So instead now, all compiler built-in headers (`stddef.h`, etc.) are
slapped into `libdyibicc.c` during packaging. So if you're embedding,
all you need is the `.c` and `.h`. It still uses the system headers (for
example, for libc) so those are still required in the normal places
(`%WindowsSdkDir%`, `/usr/include`, etc.).

### Miscellaneous updates

Additional grab bag:
- added continuous integration with github workflows thing[^2]
- moved the todo list out of main.c [to github](https://github.com/sgraham/dyibicc/issues)
- made some more [Windows headers
  work](https://github.com/sgraham/dyibicc/commit/442affc9bf76e696d5afd5c8cf92a5d58408fe05)
  that I apparently hadn't happened to include before
- surprisingly, found a [bug in the compiler's
  HashMap](https://github.com/sgraham/dyibicc/commit/3cda30d4ab74d5607e5cee3b35b671e4b6d4bbd6)
  that dated way back to chibicc's initial implementation.

### Worse ideas

As a particularly lazy fellow, especially when prototyping, I'm annoyed
and tired every time I have to make some janky linked list or `MyObj
objects[MAX_MY_OBJS]`. So in a fit of hubris, I decided to build
containers directly into dyibicc as a language feature.

Now what does it mean to be a language feature vs. just a built-in
library? To me, I think it means "syntax", and that's where we veer into
this being a questionable idea.

There are a huge number of **Absolutely
Fine** container libraries for C with various tradeoffs
([ctl](https://github.com/glouw/ctl),
[Klib](https://attractivechaos.github.io/klib/),
[mlib](https://github.com/P-p-H-d/mlib),
[sgc](https://github.com/red0124/sgc),
[STC](https://github.com/stclib/STC), and hundreds more). I
semi-arbitrarily picked STC as being featured-enough, but not too heavy.

As with all C libraries, it's necessarily a bit "stutter"-y (especially
with more complex types) as you need to repeat the namespace, the
type, and the object in each function call.

#### methodcall

To try to make this nicer, I added some extensions to dyibicc. The first
is a pretty simple one: `__attribute__((methodcall(PREFIX)))`. This is
an attribute that goes on a struct declaration that makes it "sort of
callable". So instead of writing:

```c
struct my_vector_type { ... };

my_vector_type my_vec = {0};
my_vector_type_push_back(&my_vec, 123);
my_vector_type_push_back(&my_vec, 456);
my_vector_type_push_back(&my_vec, 789);
```

you can instead write:

```c
struct __attribute__((methodcall(my_vector_type_))) my_vector_type { ... };

my_vector_type my_vec = {0};
my_vec..push_back(123);
my_vec..push_back(456);
my_vec..push_back(789);
```

The `..` syntax and `methodcall` attribute work together, and if the
static type of the left-hand side has a methodcall attribute, the
right-hand side is rewritten using the `PREFIX` and a "self" argument.

That is, with `methodcall` on the vector type, `v..push(1)` is rewritten
to `my_vector_type_push(&v, 1)`.

Additionally, `..` follows pointers, so this works as expected, without
needing to use `->` or `(*x)`.

```c
int myfunc(my_vector_type* x) {
  x..push_back(14);
}
```

I thought about using `.` instead of `..` for this, and while ambiguous
(vs. normal struct field access) I think it could probably work fine. I
wasn't sure if it'd be more or less confusing, and this was slightly
easier to implement for now.

#### Templating

The second simplifying feature was to make the "templating" part
automatic. In STC, you need to pre-`define` various `i_*` keys, then
include a specific header which generates the associated structures and
functions and then undefines those keys. So you need to figure out which
types you want to use up-front and predefine them, and think about how
they're going to be forward declared between translation units, and so
on.

dyibicc has `$vec` and `$map` built in now, which deal with this
automatically, so you can write `$map(int, char*)` or `$vec(int)` and
the correct types will be instantiated and declared (or not) as
necessary: [simple
test](https://github.com/sgraham/dyibicc/blob/main/test/container3.c)
(notice no `#include`s). Assuming this doesn't feel terrible after using
it for a while, I guess probably a string type and maybe a set type
would be commonly useful too.


#### whyyyyy would you do this

There are **many** good, valid, *correct* arguments **against** doing
this. Primarily, it just isn't really a C compiler any more, and your
code isn't going to work in another C compiler. Or maybe you just think
it's ugly! But what good is compiler power if you're not going to abuse
it! So I'm going with [Embrace, Extend,
Extinguish](https://en.wikipedia.org/wiki/Embrace,_extend,_and_extinguish)
for now. Surely domination of the C compiler market is just around the
corner.

### End

Paraphrasing the funniest email signoff I've received in a while: There
can't possibly be a better way to end a blog post!

---

[^1]: In my defense, while many issues were my bad (or more often lazy) code, some were inherited from chibicc.

[^2]: Always fun to iterate on "yaml scripting" without being able to run the actions locally so you have to make piles of trivial commits to check for typos.
