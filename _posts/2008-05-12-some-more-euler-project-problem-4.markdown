---
layout: post
title: Some More Euler Project, Problem 4
---

This one was pretty straightforward.

> A palindromic number reads the same both ways. The largest palindrome made
> from the product of two 2-digit numbers is 9009 = 91 × 99.
>
> Find the largest palindrome made from the product of two 3-digit numbers.

The hardest part was just reversing the number to be able to tell if it was a
palindrome. Unfortunately, when I searched for &#8220;reverse string f#&#8221;
I got <a
href="http://basildoncoder.com/blog/2008/04/21/project-euler-problem-4/">http://basildoncoder.com/blog/2008/04/21/project-euler-problem-4/</a>
which while certainly a good search result, could have ruined the fun. Anyhow:
the solution to reverse (why the heck isn&#8217;t there a .Reverse on the .net
string anyway?) is the obvious thing. The only thing notable thing here is the
&#8220;:string&#8221; on the argument to the function which is the first time
I&#8217;ve had to write a type other than the type coercions from float
&lt;-&gt; int. It reminds me of the irritating problem with C# generics where
it&#8217;s often not possible to write the generic function because it has to
be completely generic, or has to implement an interface so the type can be
where-constrained (or in other words, generics are generics, not templates,  I
guess. The C++ approach definitely has benefits, sometimes, though.)

{% highlight ocaml %}

let rev (s:string) = new string(Array.rev(s.ToCharArray()))

{ for i in [100..999] do
    for j in [100..999] do
        let x = i * j
        if x.ToString() = rev(x.ToString()) then yield x }
|> Seq.fold(max) 0

{% endhighlight %}

After that, it&#8217;s pretty simple. I just make a list of all the
palindromes created from 3 digit multiplicands, and then fold out the maximum
of those. I noticed something very dumb in the last solution, I was folding an
anonymous function that just directly passed its arguments to max, which is of
course silly. I&#8217;m finding F#&#8217;s syntax a little weird, but getting
better.

It occurs to me after reading Mr. Basildon&#8217;s solution that I don&#8217;t
know the difference between Seq, List, etc. and when it matters. Maybe
it&#8217;s just that seq can be infinite, vs. List is strictly an actual
memory block?
