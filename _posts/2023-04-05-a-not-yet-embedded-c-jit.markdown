---
layout: newpost
title: A not yet embedded C JIT
---

After getting the absolute bare bones of a [C
JIT](https://scot.tg/2023/03/29/c-jit/) working, I wanted to try to
embed it in a small 2D game engine. When I tried to do that, it was clear
it needed some re-organization to be a pleasant concise embedding that
didn't require the embedder to know the full internals of the compiler.

## Embedding

I started setting it up to have injectable configuration (function
pointers for output, function binding, etc.) and that made things a
little better. But that was sort of puttering around the edges, avoiding
the **big** pink elephant. That elephant is that the compiler was very
much designed as a unix-style tool where it reads from a file, writes to
a file, `calloc()`s without `free()`ing, and `abort()`s or `exit()`s when
there's a syntax error.

That sort of memory allocation and error handling strategy is very
sensible and works great in that context! Any OS newer than circa
Windows 95 is very good at cleaning up file handles and the heap without
any fuss. But, I'm trying to have an all in-process library that
compiles, links, and runs user code. An important part of compiling[^1]
is reporting errors without calling `exit(1)`.

Some approaches I tried or thought about to resolve this:

- Naively replace `exit(1)` with `longjmp` back to the entry point and cross
  your fingers. Not surprisingly this resulted in sadness.
- Take a `chrome.exe --process-type="renderer"` strategy. When the
  library wants to compile, the library would launch its host .exe with
  a special command line flag, and the host exe would have some code at
  the top of its `main()` to dispatch back to the library. This is sort
  of like a Windows version of forking without needing another binary.
  That would probably be done for the compile steps, and then the link
  would be done in-process. This approach would also necessitate a bunch
  of process spawning logic and dependency management. It also feels
  like "surrender", but I may yet submit to that approach.
- Try harder to identify all hidden state, statics, etc. and write
  "reset" functions, so that `setjmp`/`longjmp` had some better chance
  of working. This meant a `module_reset()` that gets called whenever
  things need to be cleaned up, and everything tries to cooperate.
- Just-actually-return-errors all the way up. At first it seems like it
  should just be a matter of doing quite a lot of typing and not a big
  deal beyond that. But when I started doing that it really seemed like
  the scope of the change was going to turn the code into a unpleasant
  mess, that would make it much more resistant to future changes.

(There may be other better ideas!)

I was most happy with pulling all globals and statics into [one large
`memset`able
struct](https://github.com/sgraham/dyibicc/blob/embedding-wip/dyibicc.h#L642)
for resetting. This has two benefits:

1. It's easy to reset the program state between compiles of separate
   translation units (another complexity due to the run-and-exit style);
1. In theory, it's just one `memset` to reset program state after a
   `longjmp`, which should make error recovery more plausible. This
   doesn't handle other resources (open files, memory allocated outside
   the special heaps, etc.) but it's most of the way there.

This also let me make a [simple embedding
interface](https://github.com/sgraham/dyibicc/blob/embedding-wip/libdyibicc.h)
that I was happy with for now.

However! When I did this, I discovered it had an appreciable **negative
performance effect**. The change is not too complicated and changes
**this**:

```
static Node* labels;

void parse(...) {
  // ...

  Node* node = new_node(...);
  node->next = labels;
  labels = node;

  // ...
}
```

**into this**:

```
#define C(x) compiler_state.x

void parse(...) {
  // ...

  Node* node = new_node(...);
  node->next = C(labels);
  C(labels) = node;

  // ...
}
```

plus adding `Node *labels` to a global `CompilerState compiler_state`
object.

In particular, there's **no pointer** being added. The address of
`labels` is still at some arbitrary offset in the data segment (just
also offset by the `offsetof(CompilerState, labels)`, so as I was doing
this, I assumed it would be neutral performance-wise.

But it very much wasn't. I didn't notice at first, but the tests went
reliably from taking 2.8s to taking 3.2s, which isn't a huge absolute
amount of time, but it's a lot percentage-wise. I tried LTCG/LTO (since
the definition of the structure is in a different file), but I [wasn't
able to get to comparable
times](https://github.com/sgraham/dyibicc/commit/8fd63c29ec6e62784b13ed109f7dd40a0573e8a3).[^2]

## Benchmarking

After going in circles there, and only sort of accidentally noticing the
perf regression, I decided I needed some compile-time benchmarks. I
could have generated some test code, but I figured it would be better to
compile real code. I picked the [sqlite3
amalgamation](https://www.sqlite.org/amalgamation.html) as it's large,
has limited dependencies, and is easy to compile (with normal,
functioning compilers, at least!).

It does, however, rely on calling Win32 functions to do work, and so
needs to include `windows.h`.

### A diversion into windows.h

There's really quite a lot of stuff in here. And it's not just sheer
volume, but more that everything is gated by a variety of conditions and
platforms, and a great number of branches and layers.

In theory, there's defines to turn off the parts the Microsoft
extensions, but I don't think anyone really cares about or uses those
(?) so they're more trouble that they're worth. e.g. Every compiler has
to define `_MSC_VER` as it switches a huge pile of things in windows.h,
and most user code also uses it as the flag to gate whether you're
compiling on Windows.

Similarly, I had to predefine `_MSC_EXTENSIONS` because otherwise common
structures like `OVERLAPPED` change their definition from using
anonymous unions to using a dummy name to make them old ANSI C. But
normal user code isn't going to have those extra `.u` and `.s` in their
source, so it's basically got to be on. But then having that define on
triggers lots of use of intrinsics from MSVC and different preprocess
branches, and things like
[`__ptr32`/`__ptr64`](https://learn.microsoft.com/en-us/cpp/cpp/ptr32-ptr64?view=msvc-170)
which, yeah...

In any case, with some hacking, and some questionable predefinitions,
and some unimplemented intrinsic stubs, and a soupçon of debugging:

```
#include <windows.h>
int main(void) {
  SetProcessDPIAware();
  MessageBox(NULL, "This is a message!", "dyibicc", MB_OK);
}
```
![A Win32 MessageBox](/images/dyibicc-message-box.png)

Yay!

### Eventually back to benchmarking

Back to compiling sqlite3... For the **unbridled hubris** of going
straight from Win32 "hello world" to trying to compile a 245256 line C
file that's 8,670,021 bytes, I was treated to a codegen assert on line
172119, in a function ominously named `sqlite3Parser`.

As it turns out, it was just a mishandling of an edge case in the
calling convention (which is nice to find!), but it required a fair
amount of staring at it to tease that out.

The next error is a linking problem resulting from splitting the logic
for data and code relocations that will need some rework in the object
files and linker. I will try to do something simple[^3] to work around
this, as I think the linker will need to be rewritten later to improve
performance anyway... but I need the benchmark to make sensible progress
on that!

## Why am I...

Some of the dark debugging holes are prone to leading one to ponder the
point of this exercise. I think I was going to make some sprites jump
around and be able to change how high they jumped without restarting the
program, but I may have missed a turn back there somewhere?

C also just isn't especially suited to updating one function at a time,
which I think is one reason there's been lots of "C repl" projects, but
not one that really caught on (at least not that I know of...). I'm
hoping that I can define a clear subset of C that can be well-supported
and still feels like C (or better) though.

---

[^1]: At least when I'm the error-prone author of said code!

[^2]: And then I ran it a bunch more times because I didn't really want to believe it, but it was reproducible.

[^3]: Hacky.
