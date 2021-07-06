---
layout: oldmain
---

### DropPic

DropPic <s>is</s> was a [really simple way to share mockups and
comps](https://droppic.com/) for designers. It takes advantage of HTML5
drag-and-drop, so all you have to do is drag files from
Explorer/Finder/Nautilus.

The backend is Python + [Tornado](http://www.tornadoweb.org/) (which I
really like). All data other than images in MongoDB, chosen mostly because it
seemed nice and easy to set up and use. I started by storing uploaded
images in Mongo, but the GridFS drivers weren't really up to it (at
least the ones I looked at). There also wasn't much benefit to doing so. So,
images and thumbnails live on the filesystem directly, and they're gated via nginx's
[X-Accel-Redirect](http://wiki.nginx.org/XSendfile). DropPic is
hosted at Linode.

The front-end is Closure Library, but not actually very many of their
widgets. Closure is a pleasant enough library to use, but I almost wish
they didn't have any docs. I have this cycle where I go to the docs
expectantly, get frustrated because they're written
"useless-Doxygen-style", and then grep the code/demos, and find the answer
quickly enough that way. There's also not a ton of examples (or maybe they're just
hard to google because of Closure's unfortunate name?) which
slows down the ramp-up time a little.

I also wrote a custom iPad review interface, using [Sencha
Touch](http://www.sencha.com/products/touch/). It's separate from the
"full" Closure-based UI but uses the same API in the backend of course.
Sencha Touch is nice and results in surprisingly snappy UIs. I ran into
quite a bit of trouble with the image-heavy gallery browser. The browser
was quite crashy, and I wasn't able to find away (short of page reloads)
to free all off-screen image data. As far as I could tell that was due
to Safari Mobile and the ridiculous 256meg that the iPad ships with,
rather than Sencha Touch though.

**Funny update**: The memory usage bug was one of the first I fixed when
I started at Google on the Chrome/WebKit team. Some day it'll ship in an
iOS browser build I geuss.

### Custom Processor

Just starting on this one... no code or diagrams released yet, but some
posts on direction:

* [Designing Hardware](/2010/02/28/designing-hardware/)
* [A New Old Processor](/2010/03/02/a-new-old-processor/)
* [The hardware side of a Lisp Processing Unit](/2010/05/31/the-hardware-side-of-a-lisp-processing-unit/)
* [Opcode Design for a Lisp processor](/2010/06/14/some-opcode-design/)

### Skulpt

Skulpt is an entirely in-browser implementation of Python. I gave it its
[own fancy website](http://www.skulpt.org/). You can find out more
information and grab the code there if you're interested. The basic idea
is that you can use Python on both the server and on the client and
share code between them. I wrote the translation from Python to
Javascript directly in the browser so that there isn't a pre-compile
step required to improve iteration time.

There's currently two development branches that I've been working on.
One was a completely-from-scratch just-start-typing where I wrote a
lexer, parser, and compiler passes in plain vanilla Javascript (they
were partially ported from the CPython implementation actually). This
worked pretty well, and kept the core of the compiler and the generated
code pretty small and tight. This branch is the one used in the demo on
[skulpt.org](http://www.skulpt.org/). This approach does make for a
rather large undertaking though!

The second branch is one based on using the CPython compiler to compile
to bytecode, and then a program to decompile from bytecode to
Javascript. This involves reconstructing the basic blocks out of the
bytecode and emulating a virtual stack during the compilation process to
recreate the flow of the Python. There's no `goto` in Javascript so it's
not trivial to map back to Javascript in general. The decompiler is
actually written in Python, and does just enough (as of this writing) to
self-compile *itself* to Javascript (executed on Python) so it can then
be run on itself in Javascript. (confused yet?)

Both compiler approaches have proved promising. I haven't decided which
way is more practical yet.

The runtime is basically the same between those two compiler approaches.
So far, the runtime includes a very small bit of the Python standard
libraries, as well as lower-level things that would generally be built
into the interpreter in other Python implementations. This includes
things like the bigint implementation, and support for basic types like
slices, sets, dicts, etc. Needless to say, emulating these in Javascript
isn't extraordinarily performant.

The main downer of the project though is that fundamentally Python is
'designed' to be slow. For example, the attribute lookups required (when
considering `__get__`, `__getattr__`, MRO, metaclasses, ...) and every
function invocation needs to check if the object implements `__call__`.
Implementing Python faithfully requires all of those checks, but because
when the substrate it's on top of is Javascript objects, each of those
checks is fundamentally quite expensive. Additionally, the extra checks
and wrappers in the generated thoroughly thwart today's
otherwise-quite-speedy Javascript JITs (V8, *et al*.).

In theory in might be possible to do a type of polymorphic inline
caching in the Javascript layer, so that some of those checks and tests
could be avoided, but I haven't gone as far as that yet (and it seems
fairly surreal to be doing that too!)

This [embarrasingly misinformed-though-correct
post](/2009/07/25/really-REALLY-wtf/) was early
in writing Skulpt when I discovered that Javascript `Object`s weren't
Python `dict`s. Oh well.

### MinGL

When compared to doing a `printf`-console application, drawing something
on the screen is way too hard in terms of setting libraries up,
initializing, etc. Often this is because there's low-level platform
access required for performance reasons.

Occasionally though, I would be happy with drawing if I only had enough
performance to draw a few hundred to a few thousand polygons. In that
case a simple software rasterizer with an OpenGL-ish API and a way to
set up a rendering window is all I want.

MinGL is an attempt to make that library. In order to make the
integration process even smoother, it's distributed as one C++ .h file
with no external dependencies.

It's not done yet, but it's coming along. The
[code](http://code.google.com/p/mingl/) is on Google Code if you're
interested, and you can read a few posts about progress.

* [Very Early Progress](/2009/11/08/mingl-very-early-progress/)
* [Basic Rendering Working](/2009/11/15/mingl-basic-rendering-working/)
* [Texturing](/2009/11/17/mingl-texturing/)

### Chrome Extensions

A couple simple browser extensions, nothing too exciting. There was
a few Firefox ones too, but they've, uh, gone to a better place
apparently. More info:

* [Tweak for Google Reader](/2009/12/09/background-open-for-reader-in-chrome/)
* [New Tab Page As Tasks](http://www.h4ck3r.net/2009/12/13/new-tab-page-as-tasks/)

My only takeaway here is that a few thousand people use these
extensions, and I think that all told, they total about 10 lines of
code. "Products" are not defined by how hard they are to accomplish,
which is something I consistently forget.

### EasyTelly

EasyTelly was a project I project attacked during my self-styled
sabbatical.

I went a little crazy and starting doing things like trying to source
hardware components while writing a complete Media Center software stack
from custom-Linux-kernel up. It was pretty similar to what
[boxee](http://www.boxee.tv/) is now. In retrospect, it was a
ridiculously high-competition market to try get into.

Needless to say, I started to run out of money before I finished that
rather ambitious project. I was also very excited about getting in on
the ground floor of implementing "C# for consoles" back at EA, so I
decided to shelve it and get a job again.

`todo; source from a backup that's probably around somewhere`

### Twin Isles

I've always enjoyed Civ-style games, and I had the urge to design one
around the same time as I got a "homebrew" cart for my Nintendo DS.

And so, Twin Isles was born.

- [pic0](/images/twinisles/pic-0.png)
- [pic1](/images/twinisles/pic-1.png)
- [pic2](/images/twinisles/pic-2.png)
- [pic3](/images/twinisles/pic-3.png)

The homebrew scene for the DS is pretty small, so I still get email
surprisingly often about this little game. It even got some
[enthusiastic](http://thoughtsfrommylife.com/article-757-Twin_Isles_-_Civilization_for_the_Nintendo_DS)
reviews. Anyway, you can [download the last
release](/images/twinisles-2.zip) (from 2007), but unfortunately my DS
card died, so I'm not able to update it.

There wasn't any decent emulators at the time I wrote it, but it seems
to work fine on the no$gba emulator (despite the name, no$gba emulates
DS also).

A number of people have asked about the
[source](http://code.google.com/p/twinisles/source/browse/), so I pushed
it up to Google code. It's a heckuva mess in the folder that I found
(lots of junk lying around, scripts for hacking up art, map editor,
 etc.), so you probably won't get much out of the game as a whole. The
code itself looks not-too-embarrassing (in
        [src/arm9/source/...](http://code.google.com/p/twinisles/source/browse/#hg/src/arm9/source))
so maybe someone will find something of use in there.

### Fluix

XNA is an excellent way to make games. I've been in the "real" game
industry for about 12 years now (yikes) and the mountains
that some teams have to shove around to get things done often blows my
mind (not to mention, tries my patience).

XNA is the exact opposite of having to move mountains. When the first
version came out, there wasn't any easy way to do 2D menus and UI. I
thought an interesting project would be to see if I could get enough of
a Flash player running on it to handle UI duties.

I'd previously written a Flash player back in ~2002 for the PS2, Xbox1,
and Gamecube, at EA, though it was in C, assembler, and quite a lot of
Perl in the pipeline (Perl was still my go-to language at the time `:)`,
and there was a CPAN library that parsed SWF files pretty well).

So, I understood the problem fairly well, and I thought doing a Flash
player would be a nice way to play with XNA. I named it
[Fluix](http://groups.google.com/group/fluix) for "FLash UI in Xna" I
think.

A couple of the interesting parts of this project where the handling of
geometry, and the handling of the script code written in Flash.

#### Files archive

Google Groups dropped support for files recently, so there's a copy of
files that used to be stored on Groups.

- [fluix-4.zip](/images/fluix-archive/fluix-4.zip)
- [fluix-aux-source.zip](/images/fluix-archive/fluix-aux-source.zip)
- [fluix-source.zip](/images/fluix-archive/fluix-source.zip)
- [Initial_Setup_Tutorial.swf](/images/fluix-archive/Initial_Setup_Tutorial.swf)

#### Geometry conversion

The rendering in Flash (at least the version that was out at the time)
is very old-school: it's 2D line loops with edges marked as fill or not,
tagged with colours, etc. and all very bit-packed into a strange binary
format. This clearly made sense back when Flash was first conceived, but
rendering that on modern graphics hardware would be very poor. So, part
of the pipeline was to convert this line list and 2D fill information to
a set of tesselated geometry and helper textures (for handling things
like gradients). It might not sound so complicated, but handling the
tesselation of scribbles was tricky business.

#### Script conversion

The Flash VM is a custom one designed by Macromedia. The easy way out
would to have been to write an interpreter for the VM bytecodes, but
since XNA only allows fully safe managed code (and may not have even
JITd at the time?) I thought a better approach was a recompiler from
Flash VM bytecode to a CIL assembly. It would be faster, and benefit
from whatever optimizations the XNA team pushed later in their toolchain
too.

This process was somewhat involved, as the CLI requires relatively
strict information about the state of the stack. For example, when
jumping between basic blocks the stack must be guaranteed to have the
correct number of elements, and correct type of elements regardless of
how it got there, and needs to be verifiable with a quick scan (see my
good buddy
[ECMA-335](http://www.ecma-international.org/publications/standards/Ecma-335.htm)
for all the details). The Flash VM and compiler is not as strict about
how it compiles.

Roughly, this involved simulating the Flash stack via a shadow stack and
intelligently merging via something like a phi-node (though I didn't
know that's what they were called at the time). I remember being pretty
pleased with myself when I got this recompilation working.

#### Pulling it together

I also wrote a Content Pipeline plugin for XNA which is just a plugin
for Visual Studio that lets you include assets into the project and
handles converting them to their final, in-game format. In this case, it
took .SWF files and munged them into textures, sounds, the required
geometry, and the runtime CIL assembly, and then packaged that all up
into a runtime loadable binary blob.

Drop an SWF into the solution, call `Load(...)` at runtime. No more
mountains to shove around.

Unfortunately, between XNA1 and XNA2 (or whenever it was that Xbox
support got added) the APIs changed, then I got busy at work and didn't
have time to keep it up-to-date. Having the assembly in the binary blob
didn't immediately work on Xbox either, because some or all of the
compiler runs on the host side.

With XNA picking up again on the WinPhone7, I should really get back
into it: fun stuff.

### Doxica

I've hated the PDF browser viewing experience for about as long as it's
existed. Sometime around 2005, browsers, server-side processing, and
bandwidth were good enough to avoid the much-loathed plugin. By the end
of 2006 I got up enough rage to try to finally solve this problem.

Doxica (`doxi.ca`) was a Google Maps-style view of `.pdf`, `.doc`, and
`.ppt` files. It did server-side on-demand conversion of source
documents to tiled images. I started with the xpdf code and wrote a lot
more code to speed things up, and handle extraction of text, selection
regions, links, and so on.

At the time I was going to need more processing than I could afford via
standard web-hosting so a bought a pair motherboards, CPUs, RAM, hard
drives, and power supplies, and mounted it all on a snazzy piece of
plywood. I had visions of doing 2U colocation (I can't get more than
~1Mbps upstream where I live), but I'm not sure if I could have found
anyone to put this scary looking thing into their rack.
   
`todo; picture`

The servers and set up are long gone at this point. The wayback machine
has some caches of home pages, but unfortunately it gets only the robot
crawler version of the linked-to pages, not the full AJAX version:
[here's the first home page it captured](
http://web.archive.org/web/20061230105910/http://doxi.ca/index.html),
and a [slightly revised version](
http://web.archive.org/web/20070324070134/http://doxi.ca/). I eventually
[gave up](http://web.archive.org/web/20070603094659rn_1/doxi.ca/),
partially because I got very busy at work, and partially because I
didn't feel like I could buy the servers and bandwidth it needed.

Upon admitting defeat, I (apparently) wrote:

> ...
> I still hate Adobe's crappy reader. I hope someone copies this idea and makes it great.
> ...

And happily, someone did, though surely unknowingly! I use [Google Docs
Viewer](http://docs.google.com/viewer?pli=1) on a daily basis (along
with
[this](https://chrome.google.com/extensions/detail/nnbmlagghjjcbdhgmkedmbmedengocbn))
and it's ever so much more pleasant than that dastardly Adobe plugin. 


### Dodge

> This one's very old, but I remember it fondly so this entry is mostly
> personal reminiscing. I worked on this during university, starting in
> 2nd or 3rd year (ca. 1997?) and "shipped" it somewhere between 1998 and
> 2000; it's not clear from the files I found while spelunking around on
> old harddrive backups.

My brother and I were obsessed with an old NES dodgeball game called
Super Dodge Ball. Many years later I tried to recreate it in 3D. It was
an on-and-off thing where I wrote lots of code (i.e. learned various
languages and APIs) under the guise of writing this game. This was one
version that eventually got to something like completed.

At the time, I didn't have access to any sort of 3D content creation
package like Maya or 3DS Max, so I wrote a 3D modelling package (for
some reason, called "Behemoth") to handle modelling, skinning, and
texturing of the players. There was also a simple scripting language
scripting language to control the AI players and the Street Fighter-like
gamepad moves to execute superpower throws. I've always hated doing
anything manual in UI, so there was a converter to go from from `.res`
(Visual Studio dialog edtior) to generate UI screens. It seemed pretty
cool at the time.

The modelling tool was written against OpenGL, but for reasons I can't
remember (performance?) the game was written to the 3Dfx Glide API. It
was a slightly lower-level GL-alike. The API is long dead now, but it
was very exciting when the first Voodoo 3D accelerator card came out and
you could get crazy fast 3D polygon rendering on a regular PC.

I found some old screenshots along with an html file with descriptions.
Fancy! Descriptions copied here for posterity. I remember thinking I was
awfully clever for "inventing" using barycentric coordinates + gouraud
in shot number 2 as UI for weighting. (Damn kids `;)`)

Anyway, some of these are quite ugly, but my modelling, texturing, and
animation skills were never a strong suit.

Behemoth (the modeller):

- [shot0](/images/dodge/behemoth/behemoth0.png) Just loaded base 20 bone structure that the skin is weighted to.
- [shot1](/images/dodge/behemoth/behemoth1.png) Imported Quake2 MD2.
- [shot2](/images/dodge/behemoth/behemoth2.png) Showing the interface for weighting vertices to bones.
- [shot3](/images/dodge/behemoth/behemoth3.png) Playing run animation: forearm and upper right leg are weighted, but the rest of the vertices are unweighted so they stay in the neutral position.
- [shot4](/images/dodge/behemoth/behemoth4.png) Shows using animation stuff to convert "Stand" into "Stand with ball". A bit hard to see what's going on, but it's neat.
- [shot5](/images/dodge/behemoth/behemoth5.png) Shows him in the middle of a ground throw (just flat shaded/fogged)
- [shot6](/images/dodge/behemoth/behemoth6.png) Linear velocity handling (also showing prev/next frames used during hand animating.)
- [shot7](/images/dodge/behemoth/behemoth7.png) Modifiying texture coordinates.
- [shot8](/images/dodge/behemoth/behemoth8.png) Scribbling in the 3d texture painter.
- [shot9](/images/dodge/behemoth/behemoth9.png) The texture for "Blade", captain of the "Marines"

Some early ones of the dodge (the game):

- [shot0](/images/dodge/dodge0/dodge0.png) One of the super shots; a sine wavy one, kind of hard to catch. The CPU player caught it this time though.
- [shot1](/images/dodge/dodge0/dodge1.png) Another ground super shot; a colourful spiral (pretty powerful). That guy's just about to get pounded.
- [shot2](/images/dodge/dodge0/dodge2.png) Here's another super from the air; it teleports around.
- [shot3](/images/dodge/dodge0/dodge3.png)
- [shot4](/images/dodge/dodge0/dodge4.png) Here's one of the starting screen in the "World Cup". You assign various powers to the players which determines the type of super shots they can do (normally there wouldn't be a whole bunch in the "Saved" slots, but I'm cheating.
- [shot5](/images/dodge/dodge0/dodge5.png) The guy in the air is the CPU.. I just thought it looked cool because of where he got caught in the throw.
- [shot6](/images/dodge/dodge0/dodge6.png) A grab of a super shot, it goes to the centre of the court and then accelerates towards the target.

And some later ones of the dodge (no descriptions on these ones, but I
believe this is roughly what it looked like when I released it):

- [shot0](/images/dodge/dodge1/dodge0.png)
- [shot1](/images/dodge/dodge1/dodge1.png)
- [shot2](/images/dodge/dodge1/dodge2.png)
- [shot3](/images/dodge/dodge1/dodge3.png)
- [shot4](/images/dodge/dodge1/dodge4.png)
- [shot5](/images/dodge/dodge1/dodge5.png)
- [shot6](/images/dodge/dodge1/dodge6.png)

Ah, nostalgia.

A funny thing I just realized is that this would be roughly the right
rendering complexity for mid-range phones these days. Maybe if I were
retired or something...
