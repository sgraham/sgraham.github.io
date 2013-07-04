---
layout: post
---

Occasionally, I have the need to load some image data. Typically, the
data can be relatively easily converted offline to raw RGB or .TGA using
[ImageMagick](http://www.imagemagick.org/). By converting ahead of time
to something simple, there's generally not much need to write
`$random_format_loader`.

But, for some stuff I've been doing recently, the data's coming over the
network, or is embedded in a larger file, so it's cumbersome to modify
it as a preprocess.

So, I'd like to be able to load JPEG, PNG, and DDS (which is basically a
wrapper around DXTn).

Tackling JPEG first, I was a little frightened of what I might be
getting into. Most places point to libjpeg which is quite a scary huge
beast. I'm sure it's mostly huge and scary for legitimate reasons
(encoding support, various obscure variants, optimizations, etc.) but
it's not something I'm interested in having a dependency on to just load
a picture.

A little hunting turned up [Tiny Jpeg
Decoder](http://www.saillard.org/programs_and_patches/tinyjpegdecoder/)
by Luc Saillard, and [NanoJPEG](http://keyj.s2000.ws/?p=137) by Martin
Fiedler. I found NanoJPEG nicer, and it's a very pleasant ~900 lines of
straight C. The resulting image from NanoJPEG looked a bit better too.

I crammed Martin's implementation into *one C++ `.h` file* that doesn't
require any supporting `.cpp`, and also hacked it up to be to my liking.

My mashed up version doesn't use any global/static data, so I guess
there's a small benefit there if you were using it in multiple threads,
but I haven't actually exercised that.

Martin's original version supports some configuration #defines for controlling
different methods of upsampling, and avoiding using use of stdlib, and so is
probably better for most people. But, here's mine anyway in case someone finds
it useful.

* [jpeg_decoder.h](/images/jpeg_decoder.h)
* [jpegdecodertest.cpp](/images/jpegdecodertest.cpp)

Lightly tested on `cl vs08 win64` and `gcc 4.4.1 x86 ubuntu`.

... PNG and DDS solutions to follow, once they're sorted out in similar
fashion.
