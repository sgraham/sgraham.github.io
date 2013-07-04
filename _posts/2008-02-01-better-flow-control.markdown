---
layout: post
---

Been poking around the Arc site; I did a quick <a
href="http://h4ck3r.net/vimarc0.tar.gz">Vim integration</a> (to allow sending
files/forms to the running Arc process), and I&#8217;ve been reading its code
a little, mostly to get a better understanding of the approach it&#8217;s
taking for html generation.<br/><br/>There&#8217;s bad and good, but
it&#8217;s certainly <a href="http://arclanguage.com/item?id=722">very
terse</a>. Here&#8217;s the Arc version of prompt, interstitial, and results:

{% highlight cl %}
(defop said req
    (aform [w/link (pr "you said: " (arg _ "foo"))
            (pr "click here")]
            (input "foo")
                  (submit)))
{% endhighlight %}

I&#8217;d written a Python library that makes things pretty terse
(there&#8217;s an example on that page), but after seeing the Arc version, I
wanted to trim it down some more. It now looks like:

{% highlight python %}
@op
def said(req):
    def result(foo):
        cede(link("you said: " + foo,
                  "click here"))
    cede(aform(result, input("foo")))
{% endhighlight %}

There&#8217;s a bit of magic going on, but it&#8217;s quite nice and
tidy I think.  Compared to the Arc version, I prefer having `foo` as a
regular argument to the handler function vs `(arg _ foo)` in Arc, but
the simpler closures in Arc allow you to avoid `cede` and the name
`result` which is a little nicer. It's pretty close to a direct
translation which I find interesting. I'll definitely be keeping an eye
on Arc as it develops, I found this an expanding experience.
