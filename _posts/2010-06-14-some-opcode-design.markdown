---
layout: post
title: Opcode Design for a Lisp processor
---

I've been thinking about trying to design and build a TTL-based
processor for the last few weeks, and specifically trying to make it
something that supports Lisp as its standard language.

Going all the way down to the level of electricity definitely opens up
the design options, perhaps way too far! It's very difficult to decide
where best to solve a problem when you're able to change everything from
word size and available hardware, all the way up through to compiler
implementation.

I've gone through about 10 each of completely different architectures,
instruction set styles, opcode encodings, word sizes, and so on.

I started with something based on Sussman and Steele's SIMPLE, then
veered off into a SECD-style machine, then explored things similar to
the PDP-11 instruction set.

Many of my attempted designs were pretty "top-down" in the sense that I
started writing assemblers and simulators for them, and got carried away
designing fancy instruction sets that were either too non-orthogonal, or
just simply way too complicated for me ever to have a chance of
implementing them in basic TTL logic. Others were just plain silly or
broken.

Here's a random brain dump of what I'm thinking now. Given my current rate of
starting over, it's not really likely that this one will be the one I
actually build, but this is where I'm at now.

RAM is 32k, divided into 2 half spaces. Pointers are 13 bits long and
address 16bit words, making for 8k addressable words. 16 registers are
mapped into the low 16 words.

Out-of-memory is sort of like a "fault" and jumps to a system provided
(or user-written `:)`) GC routine.

Embedded description of opcodes and encoding (or
[external](http://spreadsheets.google.com/pub?key=0AreKWASMXkZTdGFrSFRBSDNPNUNwRXc4WWlsRjlGVVE&single=true&gid=0&output=html)
if that sucks).

<iframe width='700' height='400' frameborder='0' src='http://spreadsheets.google.com/pub?key=0AreKWASMXkZTdGFrSFRBSDNPNUNwRXc4WWlsRjlGVVE&single=true&gid=0&output=html&widget=true'></iframe>

It's pretty PDP-11-y, but simpler, and the modified to my liking. `cons`
is a basic instruction, and `car`, `cdr`, `rplaca`, `rplacd` have one
instruction implementations too.

I never got around to properly writing up older designs, but some of the
code is [here along with some mumbly text files about design for various
versions](http://code.google.com/p/lpu/source/browse/).
    
`main.lisp` simulates one design (based on SIMPLE), which uses Lisp tree
structures as the basis for evaluation, as opposed to the usual linear
stream of instructions. Type bits in the pointers are things like `if`,
`lambda`, etc.

`opcodes.lisp` & `as.py` simulate a different custom design. It's sort of
an accumulator design, but most operations can be accumulated to A *or*
D, and then in some cases, A and D are treated as one register for
simple cons-cell handling.

I haven't written a simulator for the version described above in the
spreadsheet, but that's next, assuming it survives the next round of
pondering.
