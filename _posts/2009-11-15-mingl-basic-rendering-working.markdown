---
layout: post
title: MinGL Basic Rendering Working
---

[Previously](/2009/11/08-mingl-very-early-progress/), I described my
motivation for doing something as silly as writing an underfeatured software
rasterizer in this day and age.

Well, I printed out the OpenGL ES 1.x specification, and I've been doing a
little banging away. Some usual suspects that are evoking rage:

- SSE sucks. As [Max](http://www.linkedin.com/in/maxburke) said on Friday, by
SSE4+, they've gotten all the way to 75% of a good vector instruction set!
- I wish there were better debugging environments on Ubuntu. I haven't tried
the native interface on MonoDevelop 2.2 yet, perhaps that'll save me.
- And of course the usual stupid C++ crap, but hey, "There are only two kinds
of languages: the ones people complain about and the ones nobody uses." so
I'll skip that for today.

It turns out that OpenGL is not greatly suited to (non-jitting) software
implementations. Even in the pared-down, less-featureful, fixed-function
version that is ES 1.0, there's an ungodly amount of insertion points where
the pipeline can be reconfigured. To avoid runtime switching in the lowest
level part of rasterization (i.e. drawing a scanline), there'd need to be
hundreds of different "shaders" for the fixed function. For example:

- vertex colour (bool)
- texture0 (bool)
- texture1 (bool)
- fog (4 possible equations)
- texture sampling method (6 different methods * 2 texture units)
- colour mask (bool)
- depth mask (bool)
- stencil mask (bool)
- all the fragment ops:
  - pixel ownership (bool)
  - scissor (bool)
  - alpha test (bool)
  - stencil test (bool)
  - depth test (bool)
  - blending (11 blend functions)
  - logic ops (16 logic ops)

This doesn't include any vertex level operations, just the fragment level, and
I'm sure I'm still missing some. That's also only for two texture units, which
is the minimum the specification allows. You'd have to do a couple more x2's
for each additional texture unit. Permuting out all the combinations, just
with what's there though is already 17,301,504 shaders! So, clearly that's not
going to work.

It's reasonable (I guess) to make all those part of a hardware pipeline for
little additional overhead, but there's a crapload of checking, testing, and
jumping going on to do that at a software level.

Another alternative would be runtime generation via JITing. This falls outside
of what MinGL is going to do. The targetted platforms include x86, x64, PPC32,
and PPC64 at a minimum which is way too much code to cram into a header.
It's also not possible to JIT on all platforms I want it to run on,
specifically Xbox 360 and PS3.

So, I guess I'll have to do something like picking 10-100 of these "shaders"
that seem like average settings. e.g. `tex0 + depth test + noblending`, or
`colour + no depth test + one_minus_src_alpha`, and so on. These will become a
fast(er) path that's hopefully used 95%+ of the time, and other settings will
have to fall back on the uber-do-all-tests-at-runtime shader.

### Progress

Lest it seem like all bad news, I have sorted my way through a good chunk of
the vertex pipeline, and have written a few of those fast-path shaders. Here's
the always exciting gouraud + unlit in this case, doing what's probably the 3D
version of "Hello, world!": a primary coloured rotating cube.

<object width="512" height="528"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=7621487&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=0&amp;show_portrait=0&amp;color=59a5d1&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=7621487&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=0&amp;show_portrait=0&amp;color=59a5d1&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="512" height="528"></embed></object>

I also stuck the code up on code.google, on the off chance you want to trick
out an SSE vector math library, or show off your mad texture mapping
optimization skillZ, [have at
it](http://code.google.com/p/mingl/source/checkout).
