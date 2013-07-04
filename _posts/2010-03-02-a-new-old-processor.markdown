---
layout: post
---

*aka* "Lisp all the way down"

[Last time](/2010/02/28/designing-hardware/) I was talking about the my
new-found excitement for designing a processor from scratch.

Clearly there's a lot of previous research and art to draw on in this
area. I started going through some ancient, and some newer.

### ZPU

There's a few decent processors on
[OpenCores](http://www.opencores.org/): cycle accurate version of Z80s,
6502s, simple x86s, etc.

There's also a neat processor called ZPU that's entirely stack based.
It's sort of assuming a pre-2000s model of computing in that RAM access
isn't (relatively) abysmally slow. It's got a very nice opcode encoding
where every opcode is 8 bits, including the immediate instruction. The
immediate opcode is "high bit set" and that pushes the other 7 bits as a
signed value. If you put 2+ immediates in the opcode stream, then the
previous value on the stack is shifted left and the new 7 bits are ORd
in, rather than creating a new stack value. The data bus is 32 bits, and
the rest of the 128 available opcodes are assigned to the various
standard operations, mostly operating on the stack items, but a few
include a small immediate value (again, only in the 8 bits) to allow a
displacement. This is used in the SP-relative indexers to allow local
variables to be accessed without a lot of pain. I poked around this
design for a while, and it's really nifty. I might try something like
this one, though it's kind of already "been done" so I'm not sure how
interesting it'd be just to reimplement that design.

### Lisp Machines and SIMPLE

I didn't get too far in my pseudo-literature review before I started
looking at Lisp Machines. It turns out the actual Lisp Machines were not
really fundamentally anything that was specifically designed to run
Lisp. They did have custom microcode, and extra pointer bits for helping
on type dispatch, or helping the GC, but fundamentally, they were
"regular" machines that ran simple microcode, had flags, PC, stacks,
registers, conditional branching, etc.

An interesting exception to this is
[SIMPLE](http://docs.google.com/viewer?url=http://dspace.mit.edu/bitstream/handle/1721.1/5731/AIM-514.pdf)
which at the very lowest level is actually an interpreter for a Lisp.
``car``, ``cdr``, ``cons``, etc. are all primitive opcodes, and
computation is modelled on eval/apply'ing a recursive tree structure.

That paper is very interesting. Looking back with 35 ***years*** future
vantage point on someone's University project is pretty humbling (well,
it's not *just anyone's* University project, but still). This is a piece
of hardware that was designed with hardware garbage collection, and
evaluating properly lexically scoped closures as a computation model.
The average environment circa 1979 would have been a machine language
monitor on a 6502, or an assembler on a Z80, or a primitive BASIC
implementation. Compared to that sort of code-writing-experience, SIMPLE
blows me away. Hell, I had to write a singly-linked list ``#define``
"class" in plain C the other day (...which is of course just plain nuts,
but that's another story).

Of course, there are some limitations to SIMPLE. Looking at it now,
limiting all memory words to homogeneous two-word cons pairs (with no
vectors/arrays) seems very constrained. This was hand-waved away by
saying that this processor could be paired with an APL processor to
handle array-based math. That it would today just be a similar NV GPU
instead doesn't say much for the advancement of our discipline.

The non-realtime GC also sticks out, though there was a paper the next
year on how to make it realtime, for some definition of realtime.
Unfortunately, that paper is only available via
<strike>HellSpawn</strike>, sorry, *ACM Digital* **HELLSPAWN**
*Library*, so I haven't read it yet. Having a process or thread block
for a GC is one thing, having the whole processor block seems very
foreign.

There's also no ALU! It's not really needed for basic evaluation, but I
think its lack is more due to wanting to demonstrate that it wasn't
necessary and saving on die space, rather than believing it didn't
belong there.

### All the way...

So, SIMPLE is the basis of my plan for a new (but very old) processor.
Lisp all the way down. If all goes well, phase 2 will be trying to lift
some of those limitations if they actually turn out to be limiting.
