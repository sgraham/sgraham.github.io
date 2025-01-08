---
layout: newpost
title: No-op compiler benchmarking
---

On the subject of trying to make a language/compiler that is "very fast
to build" (for whatever definition of that makes sense to you)...

It seems like you pretty much have to start at the parse/lex (at least
in the spirit of all good, unnecessary projects!). I extended the dumb
script I wrote [last time](/2024/12/20/60-fps-compiler/) here
[https://github.com/sgraham/dumbbench](https://github.com/sgraham/dumbbench).

It generates a not-at-all realistic file of similar contents in various
flavours: C, Python, Lua, JavaScript, and Luv (my toy language). At
first I'm trying to test lex/parse, but most compilers aren't going to
expose that. So I just tried to use whatever flags seemed the most
"early out" that I could find, just to get an order of magnitude for
each.

All the files are unrealistically large at 10,000,000 lines (according
to `wc -l`) and vary in size from 193M to 237M depending on the
language's syntax. The Lua one had to be split up in to multiple
subfiles (all `dofile`d by the main file) as the implementations have
small fixed size limits on what it calls `chunks`, but I think it's
still a fair test as it still has to process all the code, and all the
symbols still end up in the same global namespace as in other languages.

As you can of course tell from the repository name, this is not a good
benchmark! But the timings surprised me all the same. All timings run on
my (midrange?) Ryzen 9 24 core 3900X desktop on Windows 11. I believe
all of these tools run this test single-threaded (or at least I didn't
see any significant > 1 core load). Other than the previously mentioned
Lua split-up, there's no `#include`-like behaviour in the test file, so
Windows filesystem shouldn't be hampering performance too much.

Also for comparison purposes, a simple Windows C program that does
`CreateFile`, `GetFileSize`, `VirtualAlloc`, `ReadFile` on these ~200M
files takes:
- 50-80ms to read the contents
- another ~80ms to sequentially scan the buffer and write a byte into an
  output buffer every 4 characters (simulating emitting a token)

So on the order of 150-200ms would be a _lightspeed_ baseline.

## C compilers

I like to live in the past! And C is fast, right!? So let's start with
C.

### msvc

I've always thought this was a pretty fast compiler, and it definitely
was faster than other options on Windows for a long time.

Running on version `19.41.34123 for x64` (and doing a syntax-check-only):

```
tim cl.exe /nologo /Zs dumbbench.c
real: 0m43.719s
```

### clang

This is the one I use most of the time nowadays, and it normally seems
pretty speedy. Similar to msvc, I compiled with -fsyntax-only (version
19.1.0):
```
tim "c:\Program Files\LLVM\bin\clang.exe" -fsyntax-only dumbbench.c
real: 0m22.156s
```

I accidentally had clang-17 in my PATH from a Swift toolchain (which I
think may have asserts enabled). Running on that one takes 2m21s for the
same parse (yikes!)

And just for the record (for comparison with `tcc` in a second) if you
actually ask clang-19.1.0 to generate a `.o` file, it seems to take about **5x
longer** at ~2 minutes.

Also notable, [a while back I measured something more (?)
realistic](/2023/04/11/fast-updates/) and msvc was quite a bit faster,
so maybe the only data here is that this benchmark is dumb. Onwards!

### tcc

I had previously switched a C-outputting project to compile with TinyCC
instead of the system C compiler, so I knew it was pretty fast. It
doesn't have a syntax-only mode that I could find, but telling it to
`-run` the code immediately, rather than generating an executable seems
a bit faster, so let's see how it does:

```
tim tcc.exe -run dumbbench.c
real: 0m11.172s
```

Very speedy, especially given that it's doing full native codegen!


## Python

On to the interpreters. I guess in theory these could be faster because
they can defer various semantic checking to runtime. But on the other
hand, maybe the languages are more featureful, flexible, etc.

I don't have high hopes for Python for this test, but I do love writing
Python, and my toy language sort of looks like Python code if you
squint, so  Python 3.9.2 x64:

```
tim python.exe dumbbench.py
real: 0m53.609s
```

Enh.


## Lua

### PUC Rio 5.4.7

This is the "real" Lua that you get from lua.org.

```
tim lua.exe dumbbench.lua
real: 0m6.359s
```

Wow, smokin' fast. And this is doing full (bytecode) codegen too, not
only a syntax check.


### LuaJIT 2.1

A very popular alternative implementation of Lua 5.1:

```
tim luajit.exe dumbbench.lua
real: 0m4.750s
```

Amazing! This got me interested in what it is actually doing. From a
little spelunking it seems to do a one pass parse in `lj_parse.c` to
generate bytecode, and after tracing, the interpreter execution lowers
to another SSA IR for machine code generation.

## JavaScript

I don't really know anything about JS, but all the browser vendors have
spent an an incredible amount of engineering effort on their
implementations, and parse speed has to be an important metric, so I
would assume this will be the fastest. 

### Bun

Given the "knowing nothing" I searched for `[fast javascript command
line]` and landed at [https://bun.sh/](bun.sh). Good? Bad? I dunno, it
seemed easy to install and ran `console.log("hi");` quickly. Bun
v1.1.42:

```
tim bun dumbbench.js
RangeError: Maximum call stack size exceeded.
real: 0m7.437s
```

Hmm, oh well. (To be clear, there's no large call stack in the code,
just a huge number of functions being defined.)

### Node

I've heard of this one too, and some awful tool apparently previously
required me to install it and it put it in my `PATH` so:

```
tim node dumbbench.js
real: 0m5.391s
```

Very fast!


## Conclusion

In worst-to-best order, no-op speed on 10,000,000 lines of code, on an
unscientific, poorly specified benchmark:

- Bun: `fail`
- Python: `53.6s`
- msvc: `43.7s`
- clang: `22.1s`
- tcc: `11.1s`
- Lua: `6.4s`
- Node: `5.4s`
- LuaJIT: `4.8s`

As I write this up, it's clear there's many things I could have done
better (other languages, other settings, etc.) but it's all kind of
silly, so I'm done for now.

Next time, I'll write about the rathole I went down trying to set myself
up to beat these times, and we can all learn how much I don't know about
SIMD!

### Addendum

Added Rust the next day: `436s` (7 minutes 16 seconds!)
