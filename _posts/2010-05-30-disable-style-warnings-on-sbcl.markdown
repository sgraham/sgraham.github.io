---
layout: post
title: Disable STYLE-WARNING on sbcl
---

When sbcl wants to tell you that it's unable to generate the best code,
or at least unambiguously compile the code you give it, it emits a
STYLE-WARNING. Generally, the warnings are things like functions that
haven't been defined, and so are things you do want to know about.

But, when you're working interactively, it spits out a warning that I
find irritating, telling you that you're redefining a function. Well,
duh, I know.

    STYLE-WARNING: redefining HOST-GC in DEFUN

I'm sure there's some sensible reason for this, but I'd still rather not
see it.

Also, in using someone else's code (perhaps written on a different
Common Lisp) there's often a spew of STYLE-WARNINGs too. For example,
I'm using
[lisp-unit](http://www.cs.northwestern.edu/academics/courses/325/readings/lisp-unit.html),
a simple testing thingy. It works nicely enough, but sbcl spits out lots
of warnings as it loads it.

I had to hunt around for a while to find the way to silence these, as it
wasn't obvious from the sbcl docs, but this is the way to nuke the
warning while `load`ing a particular file. For example, with lisp-unit:

{% highlight cl %}
(declaim #+sbcl(sb-ext:muffle-conditions style-warning))
(load "lisp-unit.lisp")
(declaim #+sbcl(sb-ext:unmuffle-conditions style-warning))
{% endhighlight cl %}

The `#+sbcl` makes it conditional for sbcl. That bit of code would fail
on other CLs because of the `sb-ext`. I occasionally run on ClozureCL
too, but it doesn't cause warnings in the same way, and I haven't had a
need to silence warnings there.

You may or may not want to wrap that `declaim` around your interactive
bits, weighing that you might miss more important warnings of course.
