---
layout: post
title: What can you do in 2k lines of C?
---

### Plain Old Awesome C
 
A few weeks ago I ran across some of [Sean
Barrett](http://nothings.org/)'s awesome C code.
 
It started with `stb_image.c` because it's just crazy useful and avoids so
much hassle in small demo programs. But that was just the gateway...
 
Check out `stb_truetype.h` too: TrueType font rendering in one ~1200
line header file. Do you remember how much of a pain in the ass it was
the last time you had to try to integrate FreeType 2? Or &lt;shudder&gt;
FontFusion? If you think about it for a second, you realize that
TrueType rasterization can't be *that* hard because printers were doing
it long ago on crappy little embedded processors, but the default is
just to fall back on the big ugly library, and then wrap it and pretend
it's not there. How about instead, just write some good code?
 
There's also `stb_vorbis.c` (a Vorbis decoder) which I haven't tried
yet, but I fully expect it to Do What I Want, if someday I need it.
 
And, on top of that Sean's released these as public domain (partially
thanks to [RAD](http://www.radgametools.com/) it seems). Not MIT or BSD,
and certainly not LGPL, GPL, or some other pain in the ass, but straight
up **public domain**. So much easier when you're embedded in Big Corp,
but even if you're not.
 
So, #1, use them. And #2, let's all copy Sean.
 
### So, what can *you* do in 1-2k?
 
Those libraries are standalone. Zero dependencies other than the C
standard library. There's no build files to screw with. There's no
licenses to get approved by your legal department\*. There's no attribution clauses to add
to your "About" box. Just all buttery working-out-of-the-box convenient
awesomeness.
 
I got to thinking: What **else** could be stuffed in 1-2k lines of plain
C?
 
- An JSON / XML / YAML parser?
- Shading?
- A database?
- A GUI library?
- A web server?
- Rendering?

Since I've been language-obsessed the last few years, my first 1-2k LOC
project is a [programming language, appropriately named
"twok"](http://code.google.com/p/twok/source/browse/). Calling it
something that sounds like poop dropping into a toilet probably means
that no one will want to use it, but that's probably for the best
anyway; there's lots of languages out there.
 
The question is, how much functionality can you get into 2k lines of
code? So far, twok's features are:

- Python-style syntax
- The "basics": arithmetic, bit ops, logic ops, functions, `if`, `for`, etc.
- Native compilation to x64 (and supporting both Windows and SysV Mac/Linux ABIs) so you can call back and forth with C code
- List syntax/manipulation
- Simple zone-based GC
- Varargs functions
- Basic structs

And, it's just a hair over **1k LOC**, and of course, all in one
easy-to-use header. My plan for the second half of the code:

- Some sort of macros
- More standard library functions
- List comprehension syntax
- Integration with the new GDB [debugging-support-for-JITted-languages](http://sourceware.org/gdb/onlinedocs/gdb/JIT-Interface.html#JIT-Interface)
- A backend for ARM, and maybe an interpreter backend for consoles

... Or other fun suggestions. I'm not sure if all of that will fit in
2k, but I think it should be close.
 
Certainly this is will not be the next C# or Ruby. And it's not as
practical as image loading, font rendering, or audio decoding. But, I
think it's interesting how much a hard constraint on size and a clear
goal helps focus and at the same time find a way to stuff in the
functionality you want.
 
*So, what awesome library could you write in 1-2k lines of C?*
 
**Do it!**
 
It's fun!

And release it as public domain.
 
Programmers everywhere will love you.

<sub>\*: yeah, I know that's probably still not true, unfortunately.</sub>
