---
layout: newpost
title: No files, better builds, and reflecting
---

Another update on the [hobby JIT C
compiler](https://github.com/sgraham/dyibicc) that
[I've](/2023/03/29/c-jit) [been](/2023/04/05/a-not-yet-embedded-c-jit)
[working](/2023/04/11/fast-updates) on.

## No files

In trying to make updates faster and not-flaky, I previously hooked the
compiler directly up to the editor's buffer via RPC. This way, when the
buffer is modified the changes to the code can be applied without
mucking around waiting for file system notifications.

But, in the previous version there was still a mostly-unnecessary step
where the `.c` file was provided over RPC, but it still generated an
object file (`.dyo`) that went to disk. Now, [the code and data are
generated directly to their final
location](https://github.com/sgraham/dyibicc/commit/acab98931f4282a50fa14a296b46f1ac0f69fd44)
in memory. There's still a small "link" step to fix up the references
between `.c` files. This made the code **simpler**, and also **deleted**
quite a bit of serialization code too. I did use the `.dyo` files for
debugging sometimes, so I might need to re-add some introspection
functionality at some point.

## Faster builds

... which leads to getting rid of the janky combination of `nmake` and
`GNU make` makefiles that I had been using to build the project. There's
now a simple [Ninja](https://ninja-build.org/) generator, which also
includes phony targets for running all the tests.

Previously, the tests had to be run sequentially because otherwise tests
that compiled a shared common `.c` file would collide with where they were
writing the `.dyo`, and would bork themselves[^1]. Since there's
now nothing written back to disk, ninja can trivially parallelize the test
running, which reduces test run time to **about 20%** of what it was before.

Additionally, there's multiple reasonable build configs, so I don't have
to keep fiddling with editing `/Ox /GL` to `/Od` or
`/fsanitize=address`.

## Amalgamation

With the in-tree build made more tidy, I was trying to figure out a way
to reference its ninja file or ~~Summon The Unspeakable Beast~~ write a
`CMakeLists.txt` to make it easy to use the compiler elsewhere. I
decided the simplest way to consume the compiler in an
embedded-into-a-larger-program context would be a single standalone `.c`
and `.h`.

This was [a bit
messy](https://github.com/sgraham/dyibicc/commit/f3d8719b1733b5ef8ba8bcaee2bf5f5ba3cad855),
but with a little rearranging and some preprocessor substitutions while
building the amalgamation, it also allows for creating an object file
that only has [four (non-static) exported functions along with a single
data structure for
configuration](https://github.com/sgraham/rdy/blob/main/libdyibicc/libdyibicc.h).

`static`ing everything under the rug isn't making the pig any
prettier[^2], but it made me happy to only see `readelf` report 4
exports, rather than linking against a big pile of hoohaa, previously
including such outstanding function names as `cast()` and `link()`.

As an aside, [mpack](https://github.com/ludocode/mpack) has an
amalgamated build like this, and is a very nicely written C library, if
you're ever in need of [MessagePack](https://msgpack.org/)'ing things
around (that's how the test shell does RPC with Neovim).

## Reflection

Once the compiler was more nicely embedded in the shell, I started
thinking about debugging. I'm sort of trying to avoid doing a standard
Attach Debugger, separate process-controlling-process that lets you
single step, set breakpoints, etc.

Partly, I'm steering away from that because of course it's a large
undertaking that involves lots of UI and threading and testing and
complexity. But also because it doesn't feel like quite the right
solution when I can just as easily edit the running code to add a
`print` as there's no waiting around for a recompile, relink, relaunch.
There will certainly be situations where I'd want to "Step In/Out/Over"
to understand the flow of code, but being able to evaluate an arbitrary
expression in a particular context is a large chunk of my debugging
desires.

So I just added prints for a while, and realized what would be nice
(especially with this being C) would be to not have to fiddle around
with a whole mess of `printf` format specifiers every time I wanted to
view something. It's not **too** big a deal for a few counters or
values, but once you've got a tree of structures, a GUI debugger with
`+` buttons to hop around in the structures is much better.

C of course, is notoriously just "code and ranges of memory" and doesn't
know or care anything about types at runtime. But! we're writing the
compiler, so now **this particular** C compiler has
[`<reflect.h>`](https://github.com/sgraham/dyibicc/blob/main/include/all/reflect.h).
That is a somewhat ambitious header name, but for now there's a single
intrisinic function named `_ReflectTypeOf(x)` that will return a
`_ReflectType*` that describes the given expression or type `x`.

I had a some moments of questioning my life choices when trying to
create the user string version of [names for types like
these](https://github.com/sgraham/dyibicc/blob/47ae33d77e512f42fb6c811e98033a13abf4d81a/test/reflect.c#L141-L144)[^3].
But after more attempts than I would admit to in a tech interview on
either side of the table, I think it's correct. -ish.

In the back of my mind while writing that was the acute awareness that
that type, and actually, most gibberish types (say, function pointers
taking a mess and returning worse) are, as far as C cares, all just **8
beautiful uncaring bytes**. Once they're jammed through a parser
and enough of a "type check" to satisfy someone that will happily
convert anything to or from a `void*`: `.quad 0` or `sub rsp, 8`.
Anyway.

## Up next

### repr to the editor

When starting on easing print debugging, at first I thought about doing
something like Python's `__repr__`. I think the functionality that's in
`reflect.h` now should allow adding something like `__repr__` or closer
to the mostly-automatic Rust `#[derive(Debug)]` (not including perhaps
some complexity dealing with string lifetimes).

Once that works, I was thinking it would be cool to have a single
keystroke that inserts a literal 🔍 directly in front of an expression.
Since we're recompiling on every buffer change anyway, it's not much
different than typing into a watch window. The compiler can do something
**&lt;handwave&gt;** to turn the funky Unicode into
`__repr__`-plus-RPC-to-editor. And, if it's serializing into a
structured format, the editor can also expand and collapse for viewing
the structures. And voila, a weird combination of `printf` and a "Watch
Window". Or maybe that won't really work at all, I'm not sure.

### .data updates?

I also thought more about updating data definitions when they change at
runtime. As previously described, only the functions and `.rodata`
(constants) are currently updated. Changes to structures apply to how
new code is compiled, but the compiler doesn't try to go back to patch
your old data that already exists in memory.

In part this goes back to C being "code plus untyped memory ranges": if
you're [`sbrk`ing](https://en.wikipedia.org/wiki/Sbrk) yourself some
memory and then saying that **these** bytes are **that** particular
structure, and then later you update the structure definition, the
compiler can't plausibly help update objects (and I don't really think
it would make a lot of sense to try).

But if you're writing a simple game and have a global array of stuff:

```c
typedef struct Particle {
  double x;
  double y;
  double x_velocity;
  double y_velocity;
} Particle;

Particle particles[MAX_PARTICLES];
```

then when you edit `struct Particle` to include a pointer to a texture
and a colour, it doesn't seem implausible that the `particles` array
could be reallocated, spread out, and the new fields zero-initialized
for things to keep working as expected.

I'm not entirely sure about the details of that yet though. For example,
if you rename `y_velocity` to `y_speed`, you might expect it to "just"
be a rename and not touch any of your data. But if you renamed
`y_velocity` to `lifetime` with the intention of that "slot" in the
structure being something new, you might expect it to be zeroed. So I
think I'll probably let that idea percolate some more. I assume
[CLOS](https://en.wikipedia.org/wiki/Common_Lisp_Object_System) or
someone solved this 50 years ago, so perhaps someone can tell me how
It Shall Work.

### Containers

Also emboldened by adding my first `_[A-Z]`-prefixed extensions[^4] for
reflection, it might be time for some sort of blessed or partly-magic
(to achieve parametric polymorphism) versions of `_Str`, `_Vec`, and
`_Dict`. Hacking away at this code really has increased my appreciation
for a carefully designed set of linked lists... but sometimes you really
do just want a vector of strings without the unpleasantness of writing
`char buf[256]; sprintf(buf, ...);` just this one-last-time.

---

[^1]: Of course, that could have been fixed in some other way, but it was never quite worth it.

[^2]: `#BestSupportingMixedMetaphorsInAFeatureFilm`

[^3]: I'm sure putting the half of the array return type on the far side of the function, and the seemingly-random extra required parens needed to disambiguate parsing made sense to **someone** in 1972. But only someone that was named `dmr`. As the old UNIX-HATERS quote goes, substituting `C` for `UNIX`: "There are two major products that come out of Berkeley: LSD and UNIX. We don’t believe this to be a coincidence."

[^4]: [Section 7.1.3](https://www.iso-9899.info/n1570.html#7.1.3) Reserved for meeeeeeeeeee! Drunk on reserved identifier powers!
