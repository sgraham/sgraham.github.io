---
layout: post
---

As is flying around today (at least in some very specific circles),
Google released the unfortunately named [Closure
Tools](http://googlecode.blogspot.com/2009/11/introducing-closure-tools.html).

There's 3 components:

- a template system,
- a "standard" library for JS (they're comparing it to STL or the JDK),
- a JS-to-JS compiler.

I can't say I care much about the template system, as I haven't had much
occasion to use a templating client-side. But, I need to look at it more
to understand what its intended uses are.

The standard library looks pretty decent. I think the most interesting
part is definitely `goog.ui.*` which appears to be most of the UI
widgets that are used in the building of Gmail, Maps, etc. There's some
[demos](http://closure-library.googlecode.com/svn/trunk/closure/goog/demos/)
via their SVN. These aren't flashy demos, but there's broad
functionality, and (I assume) broadly cross-browser tested support here,
which is a huge time saver.

And the compiler. I've been using the popular YUI compressor on
[Skulpt](http://www.skulpt.org). It's easy to use, robust, and gives
good compression results.

The Skulpt code seemed like a good test for the Closure compiler. Below,
"selfcomp.js" is a debug build of Skulpt (written in Python)
compiling itself to JavaScript. This results in a pretty big JS
file, weighing in at about a meg. Not unreasonable for a full
application though, given that the debug build is heavily commented,
and we're talking pre-minification.

Below is the transcript of a quick Closure compiler test.

    ~/skulpt$ ls -l support/tmp/selfcomp.js 
    -rw-r--r-- 1 sgraham sgraham 965008 2009-11-05 00:21 support/tmp/selfcomp.js

    ~/skulpt$ time java -jar support/yui/yuicompressor-2.4.2.jar support/tmp/selfcomp.js \
        -o yui.js
    real	0m6.340s
    user	0m8.393s
    sys	0m0.172s

    ~/skulpt$ time java -jar support/closure-compiler/compiler.jar --js support/tmp/selfcomp.js \
        --js_output_file closure.js
    real	4m21.287s
    user	4m27.177s
    sys	0m1.660s

    ~/skulpt$ time java -jar support/closure-compiler/compiler.jar --js support/tmp/selfcomp.js \
        --compilation_level ADVANCED_OPTIMIZATIONS --js_output_file closure_adv.js
    java.lang.RuntimeException: java.lang.RuntimeException: INTERNAL COMPILER ERROR.
    ...

    ~/skulpt$ gzip closure.js 
    ~/skulpt$ gzip yui.js

    ~/skulpt$ ls -l *.gz
    -rw-r--r-- 1 sgraham sgraham 24459 2009-11-05 19:11 closure.js.gz
    -rw-r--r-- 1 sgraham sgraham 40814 2009-11-05 18:31 yui.js.gz

Yeah, almost *four and half minutes* to compile vs. 6 seconds for the
YUI compressor. I mean, that's *fine*, it's not like you're doing it on
every change, but it's still long enough to be irritating. It's as bad
as linking on the PS3 or 360!

I haven't tracked down why the ADVANCED_OPTIMIZATIONS version doesn't
work yet. I'm sure that's a fixable problem and/or something in the
Skulpt-generated code that violates the assumptions that
closure-compiler uses. Not too worried about that.

Speed improvements however, would definitely be welcomed.

But, even without the "advanced" optimizations, the end result
post-gzipping is pretty awesome. In this case it's only 60% of the size
of the YUI version which is damn impressive.

### Update

I was missing some extern declarations that caused the ICE. With those,
the advanced version completes successfully, and I'm getting damn near
close to a 50% reduction compared to YUI.

    -rw-r--r-- 1 sgraham sgraham    21091 2009-11-05 20:48 closure_adv.js.gz

