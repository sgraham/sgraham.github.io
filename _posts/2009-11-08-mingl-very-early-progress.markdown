---
layout: post
title: mingl Very Early Progress
---

On Friday at work, I was very irritated with the state of rendering for
demo/sample purposes. Of course at EA, there's a vast array of snazzy
engines that do asset management, post processing effects, particles,
etc., etc., and are heavily optimized for the consoles and DX9+
platforms.

Unfortunately, all of this nifty functionality means that these
quite-large libraries need to interoperate and depend on other
subsystems so that they can be shared across a variety of game titles.
As a result they have a huge number of dependencies, and an enormous
footprint in conceptual API to master. The large number of dependencies
means a lot of adapters to write or find and then integrate.

In practice what this means is that setting up a new test application is
a lot of work. This in turn means that someone is more likely to slap
the code for their mostly-separable library into an already-existing
game, rather than keeping it a functionally separate library as soon as
a demo or example program requires any rendering functionality.

Which is where we get to the point of this post. On the way home I was
thinking "How hard can it be to write a simple, no-dependency rendering
library?".

What I came up with was "mingl". Its goal is to be the SQLite or Lua of
rendering very simple scenes. I want it to work on "all" platforms, for
some definition of all, not require any configuration at all on any of
those, and be simple to understand, maintain, and integrate. Continuing
the parallel with SQLite and Lua, it certainly isn't going to be the
fastest or most featureful rendering library. No one will be shipping a
game with this library.

What I've started with is a software-only implementation of OpenGL ES
1.0. It might seem like madness, and perhaps it is, but if it's
distributable as one `.cpp` and one `.h` that you slap into your project
to render some triangles, I'll be a happy guy. (In fact, I might try to
cram it all into inline classes to get it down to just a `.h`).

On that note, I've poked around for two evenings now and I've got enough
of the API roughed in, along with a texture mapper that would make John
Carmack, Michael Abrash, Chris Hecker, et al. cringe. If you don't
recognize those names from the days of yore... well, let's just say it
ain't going to win any speed records. But hey, it's (just barely)
working:

[![Thumbnail of first working texturing in mingl](/images/texturing-working-thumbnail.png)](/images/texturing-working.png)
