---
layout: post
title: FSharp and Project Euler
---

I was vaguely looking for something that might make me smarter, wouldn&#8217;t
be at all practical, and also wouldn&#8217;t be a huge time investment.

I started by working through the exercises of &#8220;Introduction to
Algorithms&#8221; by C/L/R, but I didn&#8217;t make it too far. Maybe someday.

Project Euler is some math/algorithmic problems that seem to fit the bill.
Since I was thinking I should learn an ML family language, I thought I&#8217;d
try to solve them in F# and see how far I got.

Without further ado, here&#8217;s problem 1:

> If we list all the natural numbers below 10 that are multiples of 3 or 5, we
> get 3, 5, 6 and 9. The sum of these multiples is 23.  
>
> Find the sum of all the multiples of 3 or 5 below 1000.

and my probably not so amazing solution:

{% highlight ocaml %}
[1 .. 999]
|> Seq.sumByInt(fun x ->
    if x % 3 = 0 || x % 5 = 0 then x
    else 0)
{% endhighlight %}

Not too hairy, but some neat bits:

\> is a pipelining operator that just changes the order of the arguments.
Rather than nesting the `[1..999]` at the end, it goes at the beginning which
makes more sense to read.

And, of course, first class functions. 

I really hate &#8220;then&#8221; for whatever
repressed-loathing-of-some-crappy-language-reason, but I&#8217;ll survive. I
guess.
