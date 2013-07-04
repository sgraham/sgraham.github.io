---
layout: post
---

There's been a lot of noise (and some light) up in The Twitters about Data
Oriented Design. [Noel
Llopis](http://solid-angle.blogspot.com/2010/02/musings-on-data-oriented-design.html),
[Steve
Anichini](http://solid-angle.blogspot.com/2010/02/musings-on-data-oriented-design.html),
Mike Acton
[e.g.](http://www.insomniacgames.com/tech/articles/0809/files/concurrency_rabit_hole.pdf),
[P&aring;l-Kristian
Engstad](http://www.google.com/buzz/mrengstad/9L1HaA3NuZS/Recently-the-debate-on-OOD-object-oriented-design),
[Niklas
Frykholm](https://docs.google.com/present/view?id=0AYqySQy4JUK1ZGNzNnZmNWpfMzJkaG5yM3pjZA&hl=en).
[Christer Ericson](http://twitter.com/#!/christerericson), [Stefan
Boberg](http://twitter.com/#!/bionicbeagle), and many others have been
having at it.

The points under discussion are well described in those, so I'll defer
to them. Read P&aring;l-Kristian Engstad's first if you want to get up to speed
quickly.

Most often, I find myself hitting one of the extremes. I either want to
use something very high-level and script-y (Python, Ruby), or something
very low-level (Assembler, C, ???).

The benefit of the high-level of course, is that you might have the
functionality magically accomplished for you by a library or language
feature. If you're forced to parse some XML, then generate an image, and
POST the result to a server, well, you're probably going to get it done
orders of magnitude sooner in a scripting language.

For in-game where you're working on code that's run every frame though,
it's likely that you're going to need to carefully design the layout
of your data.

In C this means focusing on getting all the data to accomplish a
particular task together into a (preferably cache-line-sized) chunk, and
grouping a bunch of those together. In C++ it naturally means the
same thing, but it also means staying true to your inner C programmer
and not getting lured by the Sirens' Song of `virtual`s up the wazoo.

My thinking is that it would be useful to make a **small extension** to
C (or C++?) that supports this method of thinking about problems. Call
it **Data Oriented C**, a strict superset of C. The goals would be to:

- encourage a more stream-centric programming model
- encourage grouping the data for a problem into little cache-sized
packets
- auto-instrument to make performance and data flow easily understood.
- support distribution of work across processors
- not be too hostile to IDEs, editors, and debuggers

What other goals do you have?

### A &rarr; A&prime;

The general idea (as espoused by Mike Acton) is that rather than
thinking of your program as manipulating a bunch of objects, think of it
as transforming data from one form to another, i.e. from A to A&prime;.

**I like to think of this as the Unix pipes model**, e.g.

    cat data | sort | uniq

This is easy to write, easy to test, and easy to understand.

Perhaps we can encourage that by supporting it more directly in the
language (*off-the-cuff arbitrary syntax*):

{% highlight cpp %}
transform ToWorld
{
    input
    {
        mat44 local;
        int parent;
    }

    output
    {
        mat44 world;
    }

    operation(int N)
    {
        for (int i = 0; i < N; ++i)
        {
            if (input[i].parent == -1)
                output[i] = input[i].local;
            else
                output[i] = output[input[i].parent] * input[i];
        }
    }
}
{% endhighlight %}

(where `transform`, `input`, `output`, and `operation` are new keywords.)

Of course, we could extend the syntax or use helper libraries to go wide
in the body of the `operation`. We could also deviate farther from C and
add more specialized `operation` styles eventually. e.g. a `map` could
elide the `for` loop, and remove the array subscripting replacing
`input[i]` with just `in` and `output[i]` with `out`. That sort of sugar
probably doesn't belong in an early version though.

### Piping

It might also be useful helpful to support a high-level syntax for
composition &agrave; la Unix pipes. Plain `|` is already taken, so
perhaps following F# for a `|>` operator:

{% highlight cpp %}
SceneNodeCollection nodes;
// ...
nodes |> ToWorld |> Cull |> PrepareForRender;
{% endhighlight %}

where `ToWorld`, `Cull`, and `PrepareForRender` are `transform`s as
defined above.

Is this necessary? Or do people generally want to hardcode the
transformation compositions, or set them up at runtime based on
configuration data?

Having the composition hardcoded allows for some improvements:

- It would allow intelligent overlapping of input and outputs to either
reduce or disallow copies.
- It would also be a good place to break into packets for DMA to
processors that don't share memory.
- It could also make for an nice place to add instrumentation for
gathering timing data.

### Implementation

Doing Data Oriented C as an extension of a plain C parser wouldn't too
hard, it could probably just be written by hand.

If it's to be an extension of C++ (probably more palatable for most
people), it doesn't seem like it would be too hard to extend
[clang](http://clang.llvm.org/) to do a source-to-source transformation
from Data Oriented C(++) to plain C(++). Realistically, that's probably
a better option for plain C too.

### Thoughts

Data Oriented C doesn't fundamentally do anything magical that you
couldn't do in C (naturally). It's all about making the [*default*
decision be the correct
one](http://nihrecord.od.nih.gov/newsletters/2009/01_23_2009/story3.htm).
It could also make it easier to help out the C compiler, for example by
correctly adding `__restrict` annotations when appropriate.

It seems like this would only be useful if it was designed by and used
across a few studios. So, what do you think? What's the feature you'd
like to see removed or added? Is the whole thing even necessary? How
would you change it? [Twitter](http://twitter.com/#!/sgraham_guid),
[email](mailto:scott.doc@h4ck3r.net), or comment below.
