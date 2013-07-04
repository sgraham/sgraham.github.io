---
layout: post
title: The hardware side of a Lisp Processing Unit
---

A couple months ago, I [was thinking about trying to build a processor
based on Lisp](/2010/03/02/a-new-old-processor/).

I got some time and motivation again to work on this (who knows where it
comes from some times). I think perhaps it was finding the
[excellently-crazy Relay Computer that Harry Porter
built](http://web.cecs.pdx.edu/~harry/Relay/). Bill Buzbee made an
[amazing and more functional computer](http://www.homebrewcpu.com/) out
of mere discrete logic TTL chips, also very impressive. (And I expect
that's the first time it's ever been described as a *more* functional
computer.)

A relay is a very big clunky version of a transistor. When power is
supplied to a control line, it activates an electromagnet, which causes
a switch on a spring to be shoved from touching one output line to
touching the other. In this way, you can cause incoming electricity go
one way or the other based on the switch.

But that's it. That's all they do.

Building a computer out of these large *things* captures the
magic of creating a computation machine out of thin air. Everyone can
understand the description of a relay, and has probably played with
magnets and electromagnets. When you string a whole lot of these
switches together and attach them in a specific way, you suddenly get a
computer? How? *<insert-Zen-moment-here>*

Somehow in the TTL version (which of course is really very similar,
except faster) it feels like the computation might be "hiding" in those
chips somewhere. Of course they're really just switches too, and
they switch much more efficiently.

Maybe it's just some silly human thing to enjoy the clicking noises that
make it feel like "It's really doing something in there."

#### Onwards

I currently know roughly nil about electricity, but was inspired enough
to think it might help things if I tried to burn my fingertips with a
soldering iron: I ordered [Make:
Electronics](http://www.makershed.com/ProductDetails.asp?ProductCode=9780596153748).

Experienced electronics dudes will probably sneer at the fact that I
also ordered [their
kit](http://www.makershed.com/ProductDetails.asp?ProductCode=MECP1) that
includes all the bits needed for the first 12 experiments. I'm sure it's
overpriced for the raw parts I'm getting, but hopefully will flatten the
learning and frustration curve, not to mention me wasting money buying
all kinds of *not-quite-right* bits.

How long can it possibly take before I'm prepped to make a relay
computer, right? `:)`
