---
layout: post
title: Project Euler, Problem 7 in FSharp
---

The problem is:

> By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6<sup>th</sup> prime is 13.
>
> What is the 10001<sup>st</sup> prime number?

Well, this sort of looks like another one that&#8217;s intended more for
pencil-and-paper solvers than programming-language solvers. But, maybe prime
\#10001 is very big, so it becomes a problem for code too. My first thought is
just to loop with a counter until we find the 10001st number, but that
involves variables which I&#8217;m apparently trying to avoid in these
problems. I didn&#8217;t get to use infinite lists in the last question, so
let&#8217;s try again:

{% highlight ocaml %}
let rec getprime(n) =
    if n = 1 then 2
    else
        let prev = getprime(n - 1)
        Seq.init_infinite(fun x -> x + prev + 1)
        |&gt; Seq.find(isprime)getprime(10001)
{% endhighlight %}

First, we assume we have the previous prime (say it&#8217;s
&#8220;11&#8221;). Then, we generate an infinite list starting at the next
number (i.e. \[12..inf]). Then, find the first number in that list that&#8217;s
prime, which is the prime after the previous one, which is the one we&#8217;re
looking for. Finally, take that functionality and wrap it in a recursion
stopping at prime #1 = 2 and we&#8217;re done.

When I first typed this code in, I messed up the initial value for the
start of the sequence as (x + prev), which of course meant it kept finding
&#8220;2&#8221; as the answer. Just a dumb mistake, but the interesting part
is that I&#8217;d forgotten I even had a debugger since I was getting so used
to using FSI to run bits of code. In the end I found the mistake by replacing
Seq.find with Seq.nth(0), and adding a couple Console.WriteLine()s.

It&#8217;d be really nice if there was a way to put focus onto the FSI tab
window though. I find myself defining functions by using Alt-Enter on the body
of the function in the text editor, and then wanting to switch to the window
to try passing it a few values to see how it works. Without a shortcut, I have
to grab the mouse, click in the right place, sometimes Ctrl-End to find the
prompt, etc. Maybe I just haven&#8217;t found the key yet, not sure.

