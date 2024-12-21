---
layout: newpost
title: 60 fps compiler
---

After tooting this: ["why isn't compiling
60fps"](https://mstdn.social/@sgraham/113676168780709161), I thought I
should check my current toy compiler project[^1] to see how it did
against this benchmark.

It's not trying to be fast at all (I am still in the "barely
understanding how to get things to work"-stage.). And it's never been
timed, in fact, I had to add the timer code to do this run.

I generated a very dumb ~10,000,000 line (188,760,025 bytes) file that
looks like this over and over again:

```
c:\src\luv0\60>wc -l a.luv
10010002 a.luv
```

```python
c:\src\luv0\60>head -15 a.luv
// This is the rllrpaq_ov_d_jcd function!
def int rllrpaq_ov_d_jcd():
    int x
    for i in range(5):
        x += i
    return x

// This is the nqvhpuaohesjgpsc function!
def int nqvhpuaohesjgpsc():
    int x
    for i in range(5):
        x += i
    return x

// This is the d_ocpwzrunuxaqst function!
```

First run in syntax-only mode (-s) which parses and typechecks, but
doesn't generate code:

```
[main]c:\src\luv0\60>..\out\luvc a.luv -r . -s -t
import: 5.7s
resolve: 5.2s
```

Not great! But probably about what I should expect given the wanton
allocation and pointer chasing I'm doing. So for syntax-only, it's about
10.9s for 10M LoC, or ~918 kLoC/s.

So let's check with codegen now:


```
[main]c:\src\luv0\60>..\out\luvc a.luv -r . -t
import: 5.6s
resolve: 5.2s
```

"... uh, not terminating"

"did it hang"

"weird"

"let's check the stack?..."

And... presenting an accidentally-very-much-worse-than-quadratic, doing
this over and over and over and over and over and over for many minutes:

```
ntdll.dll!memcpy+0x1d3
ntdll.dll!RtlReAllocateHeap+0x9ce
ntdll.dll!RtlReAllocateHeap+0x197
ntdll.dll!RtlReAllocateHeap+0x5a
luvc.exe!_realloc_base+0x73
luvc.exe!str_catlen+0x3f
luvc.exe!str_catvprintf+0x8b
luvc.exe!str_catprintf+0x1c
...
```

I let it run over dinner and it eventually did finish (correctly).

```
[main]c:\src\luv0\60>..\out\luvc a.luv -r . -t
import: 5.6s
resolve: 5.2s
codegen: 9002.7s
cwrite: 0.8s

```

So... yeah. /facepalm There's probably "a few" things I could work on
before trying to "data-orientate" my `Token`s and `Node`s to cram into
32 bits, etc. lolz.

A well-placed `str_reserve()` brings it down to:

```
[main]c:\src\luv0\60>..\out\luvc a.luv -o a.c -t
import: 5.6s
resolve: 5.2s
codegen: 28.7s
cwrite: 0.8s
```

which is... still quite bad (~248 kLOC/s), but at least semi-plausibly
fast enough to try to work on!

---
[^1]: I will write about that more at some point. I haven't let the code escape my computer yet because it's ugly and terrible.
