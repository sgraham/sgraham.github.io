---
layout: newpost
title: Foam Sandwich
---

I've been looking at this [bike camper](/2022/09/09/bike-trailer/) idea
some more. I realized that it tickles my brain because it's sort of an
insoluble problem. There's so many axes to simultaneously optimize, and
many conflict. For example, strength vs. weight for towing, cost vs.
not-spending-a-ridiculous-amount-on-a-silly-idea, large sleeping space
vs. drag while towing, etc. As a bonus, it's also 100% un-useful and
impractical which always makes things more fun!

Standard little "foamies" are built from XPS (pink/blue rigid
insulation), Titebond II glue, canvas cloth, and coats of exterior
paint. Depending on the size and shape, there's generally additional
support pieces made using traditional wood, aluminum, or steel.

For a bike trailer in particular though, and preferably non-ebike, I'd
like to really emphasize the "lightweight" axis while still keeping it
usable.

So! I'm learning what I assume is some first-year engineering. That is,
Real Engineering that involves atoms, not the pretend software-style
that largely concerns itself with trolling on Twitter[^1] while waiting for
the linker.

(I apologize in advance if I use engineering terminology improperly
and/or butcher your discipline, please feel encouraged to send
corrections.)

XPS rigid insulation (foam) has very good compression strength, and so
it's a great material if any forces applied to it are spread out. But
the surface isn't very tough (sort of squishy on top, and pieces easily
chip off), and it's quite flexible and will yield and crack very easily
unless it's extremely thick. So, the good points:
- compression
- lightweight
- water resistant (non-rotting)
- easy to work glue, cut, shape

Another material used in place of fibreglass or canvas (by RC plane
makers, I believe) is kraft paper. This is moderately thick paper,
pretty much like a brown paper shopping bag from the grocery store.

When this is stuck to the foam, it gets surprisingly much more rigid. So
I'm attempting to _Do A Science_ to get a guess as to whether a trailer
made out of _only_ foam, paper, glue, and paint would be durable and
lightweight enough to be useful.

The first round of tests are intended to get an idea of how the tensile
strength is improved. I did this by setting up pieces of 3" by 24" foam
that's 1" thick.

The kraft paper is first wetted down, a layer of glue applied to the
foam surface, the paper laid, then more glue applied to the top of paper
and then rolled in. For the multiple layer samples, the lower layers are
allowed to fully dry (24h+) before doing the next layer.

This all results in a delicious foam and paper sandwich.

How does this affect the tensile strength? Imagining that you're pushing
down on the middle, the sandwich helps because the paper doesn't stretch
(very much). This means that the bottom side of the foam can't get
longer and the top side can't get shorter (at least until the sandwich
breaks in some way), so it makes it less bendy.

To measure how well this works, the test pieces are laid across a gap as
if they were a bridge and put a weight on the very middle of the span,
measuring how much it bends (deflects).

![Deflection untreated](/images/foam-deflection-untreated.jpg)
*Measuring deflection of an untreated foam sample*

![Deflection kraft single layer](/images/foam-deflection-kraft.jpg)
*Measuring deflection of a foam sample covered in kraft paper*

Starting with untreated, measure the distance from the table to the foam
with and without one and two pound weights added. This is also done
twice flipping the sample over, and taking the average because the foam
tends to have a natural bend one way or the other.

I repeated these measurements with various samples:
- foam covered with 1 sheet of kraft paper on both sides
- foam covered with 2 sheets of kraft paper on both sides
- foam covered with 2.6 oz woven fibreglass
- foam covered with 1 sheet/2 sheets of kraft paper (i.e. an extra layer on one side)
- foam covered with 2 sheets/3 sheets of kraft paper (i.e. an extra layer on one side)

In all cases, the covers are attached with Titebond II glue, in
particular for the fibreglass -- it's not using resin or epoxy, it's
just glued on too.

Here's the raw deflection data.

### Untreated

| Nominal | 1 lb | 2 lb |
| ------: | ---: | ---: |
| 3.5405 | 3.0680 | 2.6805 |
| 3.5115 | 3.0980 | 2.7355 |

### Kraft 1/1

| Nominal | 1 lb | 2 lb |
| ------: | ---: | ---: |
| 3.3840 | 3.3425 | 3.3100 |
| 3.6470 | 3.5475 | 3.4795 |

### Kraft 2/2

| Nominal | 1 lb | 2 lb |
| ------: | ---: | ---: |
| 3.9165 | 3.8750 | 3.8220 |
| 3.1490 | 3.0895 | 3.0415 |

### Fibreglass 2.6 oz

| Nominal | 1 lb | 2 lb |
| ------: | ---: | ---: |
| 3.6415 | 3.5830 | 3.5195 |

### Kraft 1/2

| Nominal | 1 lb | 2 lb |
| ------: | ---: | ---: |
| 3.5790 | 3.5295 | 3.4810 |
| 3.5340 | 3.5115 | 3.4740 |

### Kraft 2/3

| Nominal | 1 lb | 2 lb |
| ------: | ---: | ---: |
| 3.4040 | 3.3635 | 3.3425 |
| 3.7310 | 3.7085 | 3.6910 |


There's two measurements for each type, testing with both sides up
because there's a curve. "Fibreglass B" is missing because I did such a
bad job of fibreglassing that the bubbles on that side made it
impossible to measure. Also note that there's substantially more
accuracy implied by the number of digits after the decimal point than
there really was.

Now, taking the raw deflection measurements, and using "untreated" as an
example, calculate the difference between nominal and with-weight. Then,
take the two deflection amounts, and average them:

$$
\begin{align}
\delta{}C_1 & = 3.5405 in - 3.0680 in = 0.4725 in \\
\delta{}C_2 & = 3.5115 in - 3.0980 in = 0.4135 in \\
\delta{}C & = (0.4725 in  + 0.4135 in) / 2 = 0.443 in \\
\end{align}
$$

So, untreated, the foam deflected an average of $$ 0.443 in $$ under a 1
lb weight.

Next, bust out the _Serious Engineering 101_ to calculate the foam's
**moment of inertia**: $$ \frac{width * height^3}{12} $$ [^2]

$$
I = (bh^3)/12 = (3 in * (1 in)^3)/12 = 0.25 in^4
$$

I assumed this was constant even though it isn't exactly. For example,
the coverings aren't zero-width.

Then use the **moment of inertia** to calculate the **modulus of elasticity**,
which is the useful thing: $$ \frac{force * length^3}{48 * I \delta{}C} $$ [^3]

$$I$$ is the **moment of inertia** from above, $$\delta{}C$$ the **deflection**
measured.

$$ E = \frac{FL^3}{48I\delta{}C} = \frac{1 lb * (24 in)^3}{48 * 0.25in * 0.443in} = 2600 PSI $$

Repeat that mess for both one and two pound samples, and for all the
candidates. Assuming I did any of that correctly, here's the PSI measurements.

| Sample | PSI |
| ------ | --: |
| Untreated 1lb | 2600 |
| Untreated 2lb | 2816 |
| Kraft 1/1 1lb | 16340 |
| Kraft 1/1 2lb | 19080 |
| Kraft 2/2 1lb | 22811 |
| Kraft 2/2 2lb | 22811 |
| Fibreglass 1lb | 19692 |
| Fibreglass 2lb | 18885 |
| Kraft 1/2 1lb | 32000 |
| Kraft 1/2 2lb | 29164 |
| Kraft 2/3 1lb | 36571 |
| Kraft 2/3 2lb | 45399 |

Because the force (weight applied) should be factored out, the 1 and 2lb
ought to be the same. For the stiffer samples, the 1lb didn't deflect
very much so the measurements were likely poorer. In any case, somewhere
between the 1 and 2lb PSI are about what I measured. So averaging the
PSI measurements again, and sorting:

| Sample | PSI (average) |
| ------ | ------------: |
| Untreated | 2708 |
| Kraft 1/1 | 17710 |
| Fibreglass | 19288 |
| Kraft 2/2 | 22811 | [^4]
| Kraft 1/2 | 30582 |
| Kraft 2/3 | 40985 |

Interestingly, this puts a single layer of kraft at almost exactly the
same stiffness as a single layer of light fibreglass. With the caveats
that I did a terrible fibreglassing job, that the fibreglass is slightly
lighter than the paper, that the fibreglass I got was very lightweight,
and that my measurements are crappy, this is still pretty cool. Also, 3
layers on the "outside" are more than twice as stiff as a single thin
fibreglass layer.

_However_, given that I **did** do a terrible fibreglassing job whereas
the kraft goes on pretty well even when applied with no skill or
practice, I feel pretty good about ploughing onward with kraft paper. My
current plan then is either one or two layers on the inside of the
structure, and three on the outside (as it's more likely to get bashed
and will be closer to water, etc.).

Speaking of water, another test I really ought to do is a more thorough
application of some sort of exterior paint to make sure it can be
waterproofed. But I think there's enough options that that exploration
can be deferred until I'm actually ready to paint. Or I'll just choose
something cheap and go for it.

I also noticed that uneven application (i.e. more layers on one side
than the other) seems to cause foam to warp, so "Kraft 0/3" probably
wouldn't work that well.

---

[^1]: In what I feel is an admirable show of self-restraint, I didn't even href any SWE's twitter to "Twitter" here.

[^2]: Just because! This is Engineering and I don't need to hear about "why are doing this?". This number goes in the next crazy formula, so we're darn well going to get it.

[^3]: Look, we're second-string programmers pretending to be civil engineers building a bridge out of foam and paper. Just plug the damn numbers in.

[^4]: That 2/2 is measured as weaker than 1/2 is not a show of strength for my data. This is likely because 2/2 was the first one I did, and I didn't wait for a full cure between layers, so it's probably more like "1.5/1.5" or worse.


<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
