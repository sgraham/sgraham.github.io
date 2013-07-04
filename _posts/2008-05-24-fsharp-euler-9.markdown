---
layout: post
title: FSharp, Euler 9
---


The problem statement:

> A Pythagorean triplet is a set of three natural numbers,
>
> a<sup>2</sup> + b<sup>2</sup> = c<sup>2</sup>
>
> For example, 3<sup>2</sup> + 4<sup>2</sup> = 9 + 16 = 25 = 5<sup>2</sup>.
>
> There exists exactly one Pythagorean triplet for which a + b + c = 1000.
>
> Find the product abc.

This is another one that&#8217;s probably really more &#8220;math&#8221;-y
than programming-y, but I&#8217;m enjoying using my new F# hammer to solve
these, so might as well keep at it.

It seems like another nice make-a-sequence-and-then-filter-it, but just doing
1..1000 for a, b, and c, results in an awfully big sequence (a billion long).
So, a couple simple observations to make the numbers a lot smaller. The main
one is that you can just make c = 1000 - a - b, since we know that all answers
have to have that form anyway.

{% highlight ocaml %}
seq { for a in 1..1000 do
        for b in a..1000 do
            let c = 1000 - a - b
            yield (a,b,c) }
|> Seq.first(fun (a,b,c) -> if a*a + b*b = c*c then Some(a,b,c) else None)
{% endhighlight %}

Voila!
