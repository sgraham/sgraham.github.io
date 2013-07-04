---
layout: post
title: Euler is streaking in F#, problem 5
---

Problem #5:

> 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
>
> What is the smallest number that is evenly divisible by all of the numbers from 1 to 20?

Speaking of infinite sequences, here&#8217;s the solution that seemed obvious
to me at first.

{% highlight ocaml %}
open Microsoft.FSharp.Math
Seq.init_infinite (fun x > BigInt.FromInt32 x)
|> Seq.find(fun (x:BigInt) ->
    x > 1I && Seq.for_all (fun (n:BigInt) -> x % n = 0I) [1I..20I])
{% endhighlight %}

Nice and simple, just iterate through all numbers, and find the first ne
that&#8217;s evenly divisible by all the numbers from 1 to 20. Unfortunately
let it run for an hour (!) while I had dinner, and it hadn&#8217;t completed.
I just assumed was doing something dumb, but it seems to give sensible answers
for the numbers in the range of 1..10 and 1..16. Apparently, at 1..17 or more
though the answer becomes &#8220;quite&#8221; large. The first version just
used int32&#8217;s rather than BigInt; I thought perhaps it was getting past
2^32 and so never finding the answer, but it&#8217;s hard to say since I
wasn&#8217;t prepared to wait any longer for the BigInt version to
finish.<br/><br/>As a side note, the bigint stuff is a bit ugly in this
example, I guess an unfortunate side effect of .NET showing through where the
numerical stack is fractured (sensibly and everything, just a little
unfortunate here).<br/><br/>In any case, a more mathematical and less
brute-force algorithmic approach seems to be required for this
problem.<br/><br/>Here&#8217;s one that takes only milliseconds to run based
on:<br/><a
href="http://en.wikipedia.org/wiki/Least_common_multiple#Alternative_method">http://en.wikipedia.org/wiki/Least_common_multiple#Alternative_method</a>

{% highlight ocaml %}
let rec numTimes(x, p) =
    if x % p = 0 then numTimes(x / p, p) + 1
    else 0
let maxNumTimes p =
    let num = float([1..20] |> Seq.map(fun x -> numTimes(x, p)) |> Seq.fold(max) 0)
    int(Math.Pow(float(p), num))
[1..20]
|> Seq.filter(isprime)
|> Seq.map(maxNumTimes)
|> Seq.fold1( * )
{% endhighlight %}

For all primes in the range, figure out the maximum number of times that prime
appears in the prime factorization of any of the numbers, and find the product
of those primes raised to the maximum number of powers. I learned a little F#
in this one, but as far as the math, it would have taken me a long while to
recall or figure that out, so it was basically just implementing what
Wikipedia described. Oh well.

My &#8220;fold&#8221; got one better again, instead of passing a pointless
anon function and a pointless initial value, last time I got rid of the
function. This time I found &#8220;fold1&#8221; and got rid of the non-useful
initial value too! :)
