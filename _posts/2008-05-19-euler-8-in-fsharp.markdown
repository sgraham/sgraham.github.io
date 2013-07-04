---
layout: post
title: Euler 8 in FSharp
---

The problem:

> Find the greatest product of five consecutive digits in the 1000-digit
> number.
>
> 73167176531330624919225119674426574742355349194934
> 96983520312774506326239578318016984801869478851843
> 85861560789112949495459501737958331952853208805511
> 12540698747158523863050715693290963295227443043557
> 66896648950445244523161731856403098711121722383113
> 62229893423380308135336276614282806444486645238749
> 30358907296290491560440772390713810515859307960866
> 70172427121883998797908792274921901699720888093776
> 65727333001053367881220235421809751254540594752243
> 52584907711670556013604839586446706324415722155397
> 53697817977846174064955149290862569321978468622482
> 83972241375657056057490261407972968652414535100474
> 82166370484403199890008895243450658541227588666881
> 16427171479924442928230863465674813919123162824586
> 17866458359124566529476545682848912883142607690042
> 24219022671055626321111109370544217506941658960408
> 07198403850962455444362981230987879927244284909188
> 84580156166097919133875499200524063689912560717606
> 05886116467109405077541002256983155200055935729725
> 71636269561882670428252483600823257530420752963450

Treating it as a number is probably not going to be too pleasant.

{% highlight ocaml %}
let prob8num = "7316 ... 52963450"
let chars = prob8num.ToCharArray() |> Array.map(fun x -> Char.code(x) - Char.code('0'))
let rec prob8 (rest : array) =
    if rest.Length     else
        let tl = Array.sub rest 1 (rest.Length - 1)
        let curProd = Array.sub rest 0 5 |> Array.reduce_left( * )
        Math.Max(prob8(tl), curProd)
prob8 chars
{% endhighlight %}

So, store it as a string, but then convert it to a character array, and map to
the actual numerical values (assuming ASCII I guess).

From that, just a simple recursive solution that does way too much
Array.sub&#8217;ing. It would make much more sense to use List&#8217;s instead
of Array&#8217;s for all of those .subs, but, there was no sub extraction
built into List so I just did it that way instead. 

I wrestled a little with the syntax of F# again in this question. I tried
putting the &#8220;let tl&#8221; as inline into the body of the call to
Math.Max, but I couldn&#8217;t get it to work correctly. Not sure what the
required syntax is, maybe I need some of the keywords that I don&#8217;t know
from non-#light yet?

Also, my copy of Expert F# has arrived, so I&#8217;m just starting to peruse
it now. Hopefully my code will become more idiomatic soon enough. 

And man, do I hate blog software&#8217;s handling of code. You&#8217;d think
that maybe if I typed a less-than sign they could figure out how to escape it
moderately properly, but apparently that&#8217;s way too complicated. Idiotic.
