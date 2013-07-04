---
layout: post
title: Really? REALLY? WTF.
---

{% highlight js %}
js> x = [];
js> x[0] = "num0";
num0
js> x[1] = "num1";
num1
js> x[2] = "num2";
num2
js> x
num0,num1,num2
js> x["1"] = "str";
str
js> x
num0,str,num2
js>
{% endhighlight %}

Someone please tell me there's a way to avoid this idiotic behaviour.
