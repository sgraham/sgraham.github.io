---
layout: post
title: MinGL texturing
---

In doing an old-school software triangle texture mapper, I've been trolling
through some old parts of the internet.

I've found a huge amount of pages (like the semi-reborn venerable [3D Engines
List](http://www.3dengines.de/src_feat_accu.html)) with pages that
have fully 100% dead links.

There's tons of references to flipcode.com and x2ftp.oulu.fi both of which are
long gone but well-remembered in some circles. The best reference I remembered
was Chris Hecker's articles in GDMag, and happily he's [got them online
now](http://chrishecker.com/Miscellaneous_Technical_Articles#Perspective_Texture_Mapping)
because I'm pretty sure my dead-tree versions are long since recycled.

(As a side note, it seems like pure *Institutional Retardation* that Chris
Hecker got laid off from Maxis.)

Anyway, today [Jaap](http://jaapsuter.com/) (apparently a dead link also right
now), was extolling the virtues of sub-texel and sub-pixel accuracy with a
righteousness that only an ex-flipcode'r could. `:)` Apparently the classic
test of whether you've got it right is to do a 1:1 mapping and then rotate in
2D, parallel to the near plane (i.e. around Z).

So, here's MinGL doing that. I believe it's right, though the test texture
causes some bad moir&eacute;. This is also quite possibly the most boring
video ever.

<object width="512" height="512"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=7656990&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=0&amp;show_portrait=0&amp;color=59a5d1&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=7656990&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=0&amp;show_portrait=0&amp;color=59a5d1&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="512" height="512"></embed></object>

For a long while last week, I was convinced that I had a bug in texel
sampling. This is a little tricky to explain, but here's the situation.

First, a few definitions. Texel coordinates on a 64x64 texture range from
`(-0.5, -0.5)` at the top left, to `(63.5, 63.5)` at the bottom right. Those
values are the extents of the *edge* of texels, so the very centre of the top
left texel is `(0, 0)` and the centre of the bottom right is `(63, 63)`.

Similarly, the screen space coordinates range from `(-0.5, -0.5)` to
`(screenWidth - 0.5, screenHeight - 0.5)` with the centre of the pixels being
integral coordinates.

Now, if want to do a *bitblt*, i.e. have the texture drawn at 1:1 as if it was
plain old 2D, there should be vertex positions where that will happen. And of
course there is: with the vertex and texture coordinates at `(-0.5, -0.5)` to
`(63.5, 63.5)`, we get a perfect 1:1 mapping. Here's a screenshot of it, blown
up after the fact:

![Nice 1:1 mapping](/images/subtexel-offset0.png) 

Not very exciting, but it is perfectly 1:1, which is the sort of thing 2D hud
artists will get all worked up about.

However, because we're just using point-sampling, it seems it should be fine
to put the geometry anywhere. As long as the size is 64x64, then there should
always be one texel per pixel regardless of whether it's offset by the same
amount. However, when I put the vertices from `(0, 0)` to `(64, 64)`, I get
this artifact:

![Screwy mapping](/images/subtexel-offset0.5.png) 

A brief digression into texture sampling...

Because we can only either light or not light individual pixels, and not
anything smaller, we want to be sure we get as close to the right colour as
possible for each pixel. Specifically, we want to sample the texture at the
texel location that represents the centre of the pixel.

The triangle rasterization calculates gradients across the triangle. One of
these is how much to step in the texture when moving across a scan line. So,
to make sure that we always sample from what would be the centre of the
pixel, at the beginning of the rasterization for each line, we just make
sure to move the running sum of deltas so that it lines up with the
centre of the pixel.

So, in the case where the vertex is also at a `-0.5` offset and we're drawing
1:1, this prestep will be `0.5`. If the vertex offset is `-0.25` then the
prestep will be only `0.25`.

However, when the geometry is exactly aligned on integral coordinates, then
the prestep is `0`. This is the "edge" (har-har!) case, where the vertex lies
exactly on the pixel centre, so there's no need to move at the start to align.
Because the texture's being drawn 1:1, we're advancing the texture coordinates
by 1 for every pixel, so we simply step along by 1, starting at 0.

It seems like the simplest possible case.

But, when actually looking up texture data the texel coordinates need to be
converted to integers, because we're just point sampling, not blending. So,
the texel coordinates have to be `ceil`d or `floor`d somewhere. So,
when we're stepping starting at zero, and adding one, we might get
sample data like:

    0.000000, 1.000000, 2.000000, 3.000000, 4.000000, 4.999999988899, 5.9999999, ...

And, in using `floor` or `truncate` or `ceil`, or anything else we've just
sampled the same texel twice when we really didn't want to. Of course, adding
a bias just masks the problem in this case, and move it to some other offset
of vertices relative to texels.

This probably woudldn't be very noticable in a fixed-point rasterizer because
then the +1 step would be stable. The problem still exists for some other
fractional value that *doesn't-quite-make-it*, but it's not when trying to do
1:1, so it probably goes undetected.

It was actually very difficult to get that screenshot of the artifact too, I
had to disable the entire transformation pipeline, and pass screen coordinates
into the texture mapper, and then try various pixel offsets.

Anyway, it's not really a practical problem because 1:1 geometry should just
be aligned properly in 2D, but I thought it was an interesting investigation.
