---
layout: post
title: Euler Problem 2 Redux
---

This is a similar attempt, not sure if it's better or worse really, but uses comprehensions instead.

{% highlight ocaml %}
{ for i in [1..33] do
      let x = fib(i)
      if x < 4000000 && x % 2 = 0 then yield x }
|> Seq.sumByInt(fun x -> x)
{% endhighlight %}
