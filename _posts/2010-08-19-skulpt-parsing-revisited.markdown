---
layout: post
---

Over and over, I "rediscover" that the easiest and most reliable way to
do something is to have an exact description of what needs to be done.

That sounds like a tautology, but when applied to code it can be very
powerful.

My latest reinforcement and example of this idea was in my renewed
attempt to get [Skulpt](http://www.skulpt.org/) back on the rails to
something that I could maintain and extend more easily.

The first time around I was a bit overwhelmed: it turns out that
implementing a full version of Python is quite a large undertaking (who
knew! `<ahem>`).

But, the thing is, there's plenty of help available. There's of course
the source code to CPython. I have referred to that quite frequently,
because when it comes down to it, that's unfortunately the only
"spec" for Python.

However, it doesn't turn out to be the most useful thing. The most
useful thing, by far, ***is the ability to generate tons of test data
that's known-good***.

The first time around on trying to write a compiler, I had done the
obvious thing of passing python code to CPython and also to my compiler,
and then making sure that running them both resulted in identical
output.

However, the crucial part that I didn't do was to mirror CPython at
***other levels*** of implementation.

As one example, there's any number of ways you could choose to implement
scoping and binding of names in a programming language. By only
comparing the run output between CPython and Skulpt I was effectively
reverse engineering a lot of that knowledge. Of course, for the common
cases, everyone knows how variables are bound, shadowed, closed over,
deleted, etc. But it's the obscure cases that need to be correct so
that everything is rock-solid, and that's where you never feel sure
that you've considered all cases in tests.

So, the ***magic step*** this time around: I made sure there was two
more levels where I could dump internal state from CPython and make sure
that it matched Skulpt's exactly. Both the AST nodes (using the [`ast`
module](http://docs.python.org/library/ast.html#ast.dump)) and
the symbol table (using the [`symtable`
module](http://docs.python.org/library/symtable.html)) now match
1:1 between Skulpt and CPython. This includes many little details that
are important but easily overlooked: line numbers and column offsets
being identical in the AST for error messages, all variables being
tagged as `free` or `cell` identically, and so on.

This was huge for my confidence in correctness. I now have the ability
to generate as much test data as I want for the AST and symbol table. I
could, for example feed all of `Python/Lib/*.py` to both Skulpt and
CPython and compare a pretty-print of the ASTs and symbol tables.

Or, in other words, *I have an exact description of what needs to be
done* in test-data form. How hard can it be at that point?

The AST and symbol table are two big chunks of the implementation of the
compiler. With confidence that they contain a correct version of all the
information required, I now have a solid foundation to build the rest.

The "rest" is compilation of the AST to `.js`, runtime support, and the
object model. More on their progress next time.
