---
layout: post
title: Project Euler, Problem 10 in F#
---


Problem&#8217;s quite simply stated this time:

> The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
>
> Find the sum of all the primes below two million.

First typed in solution was simply:

{% highlight ocaml %}
[2..1999999]
|> Seq.filter(isprime)
|> Seq.fold1(+)
{% endhighlight %}

Which got me a number pretty quickly that looked lovely, but was completely
wrong. I ran it again, apparently hoping that&#8217;d it magically be right
the second time. Then I tried for those below 1000000 instead and the sum was
negative. Oops! So, the quick fix and working version (changing the
&#8220;int&#8221; range to &#8220;bigint&#8221; range):

{% highlight ocaml %}
[2I..1999999I]
|> Seq.filter(fun x -> isprime(int x))
|> Seq.fold1(+)
{% endhighlight %}

I wonder if there&#8217;s a checked-overflow-arithmetic version of F#? Might
be useful for some of these questions, since they&#8217;re so computationally
light anyway.
