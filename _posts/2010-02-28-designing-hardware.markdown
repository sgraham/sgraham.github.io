---
layout: post
---

[Dave](http://dwcope.freeshell.org/projects/) and I both did the
[NAND-to-Tetris](http://www1.idc.ac.il/tecs/) course a while back. Actually, I
believe Dave did the whole course, but I stopped around the "compiler"
assignment because it was too close to what I was doing at work at the time to
be entertaining.

The course was geared towards very beginner CS students which is great. It
gives a nice vertical slice of all the bits and pieces that go into getting
your average piece of code to run, and did it all in a way that was simple to
follow along with. The assignments and test cases given were excellent in the
way they walked you down the garden path very clearly, but you still felt like
you were "figuring it out" yourself.

I work firmly in the realm of software, but that course was enough to catch a
bit of the hardware bug and have me wanting to venture below machine code.

I found a few nifty/slightly crazy attempts to recreate pre-Z80-era micros
(like [Magic-1](http://www.homebrewcpu.com/) and [Mark 1
FORTH](http://www.holmea.demon.co.uk/Mk1/Architecture.htm)). Those two are
particularly crazy in that they don't use any microprocessor. The largest IC
they use is a 4-bit adder, and everything is built up from TTL 74xx series
chips (basically just and/or/flip-flops/etc.). I was all amped up to try to
build something similar, but looking at some [wire wrap
pictures](http://upload.wikimedia.org/wikipedia/commons/d/d1/Computerplatine_Wire-wrap_backplane_detail_Z80_Doppel-Europa-Format_1977.jpg)
and then watching Bill Buzbee's [bring-up attempts of his
CPU](http://www.youtube.com/watch?v=6UT1arQ5RNs) pretty much scared me off of
that idea. They look extremely cool, and I'm duly impressed, but that's a
whole lot of tedium I'm not quite prepared for yet.

So, I started looking into FPGAs. Doing a CPU on FPGA isn't nearly as cool as
having your own wirewrapped CPU. Mostly because it'll just look like some
generic standard board, so when the victorious moment arrives when it finally
prints "``Hello, World``" or the answer to ``fib(7)`` over a serial cable,
onlookers may not be as impressed as they ought to be.

However, it does turn hardware into a (relatively)
non-tedious/not-too-expensive project, so I think I'll go that way. My other
excuses are that I don't have a serial port on my computer, and TTL chips are
hard to find nowadays. [This FPGA beginner dev
board](https://www.digilentinc.com/Products/Detail.cfm?NavPath=2,400,792&Prod=S3EBOARD)
has a bunch of nifty connectors, and isn't too expensive. They have others
that are cheaper too, with less connectivity.

Next time, my take on trying to come up with an interesting processor that
isn't just a generic RISC clone.
