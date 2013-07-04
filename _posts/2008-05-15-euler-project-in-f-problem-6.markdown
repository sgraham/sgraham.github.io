---
layout: post
title: Euler Project in F# Problem 6
---

Kick it, Euler:

> The sum of the squares of the first ten natural numbers is,
>
> 1<sup>2</sup> + 2<sup>2</sup> + &#8230; + 10<sup>2</sup> = 385
> 
> The square of the sum of the first ten natural numbers is,
>
> (1 + 2 + &#8230; + 10)<sup>2</sup> = 55<sup>2</sup> = 3025
> 
> Hence the difference between the sum of the squares of the first ten natural
> numbers and the square of the sum is 3025 - 385 = 2640.
>
> Find the difference between the sum of the squares of the first one hundred
> natural numbers and the square of the sum.

Not much to this one. I learned about the exponentiation operator which seems
to be a rewrite to calling a Pow method (it doesn&#8217;t seem to work on
int). Here&#8217;s a &#8220;my brain is currently warped into thinking about
everything as a sequence and operations on sequences&#8221;-solution:

{% highlight ocaml %}
([1.0..100.0] |> Seq.fold (+) 0.0) ** 2.0
- ([1.0..100.0] |> Seq.map(fun x -> x*x) |> Seq.fold(+) 0.0)
{% endhighlight %}

See y&#8217;all next time.
