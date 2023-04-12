---
layout: newpost
title: Fast updates
---

## We regret the error...

From [last time](/2023/04/05/a-not-yet-embedded-c-jit/), there was
indeed no performance problem with adding a (non-pointer) global to hold
state. The problem was that I mashed another separate change into that
work which accidentally turned the heap into .bss data. And having the
loader have a whole heap to zero out before starting `main()` is not the
best way to improve performance.

With that egg wiped off my face, onwards!

## Compile timing

Once I got the C JIT [to get to the main prompt of
sqlite3](https://twitter.com/h4kr/status/1643837668294553601), I wanted
to check compile times vs. the no-opt build in `clang` and `cl`.

### dyibicc
```
c:\src\dyibicc>timavg dyibicc shell.c sqlite3.c
...
avg = 0m1.722s
      1724920us
```


### clang 15 -O0
```
c:\src\dyibicc>timavg clang -O0 shell.c sqlite3.c
...
avg = 0m2.868s
      2868713us
```

### msvc 2022 /Od
```
c:\src\dyibicc>timavg cl /Od /nologo shell.c sqlite3.c
...
avg = 0m0.850s
      848077us
```

`cl` is very quick![^1] A [quick
profile](http://www.codersnotes.com/sleepy/) and a few small tweaks to
string processing got dyibicc down to `avg = 0m1.478s`, but there's
still a big gap there to the no-opt cl time.

I went off on a tangent setting up profilers and Deciding What Must Be
Done to be faster than `cl`, but... that's kind of boring when you don't
have an actual real target to optimize. sqlite3 is a good test case, but
it's weird (two enormous files), which stresses the tokenizer and
parser, but not e.g. include path searching. I tried generating other
test cases that were the opposite (many files, many includes, etc.) and
those showed different bottlenecks. But short of "optimize everything",
none of it seemed especially bad, or in obvious need of fixing first.

## Faster updates instead of faster compiles

So instead, I decided to continue on the embeddability. With the
compiler's state mostly bundled up successfully, I took another go at
`longjmp`ing [out of error
conditions](https://github.com/sgraham/dyibicc/commit/76b60aeaa64667361c2e7ec13c633664b2ae1ff6).
There are undoubtedly corner case footguns that will get me later, but
it actually seems to work well in practice after a bit more debugging.

Once that seemed to be working, I made a [small shell
app](https://github.com/sgraham/rdy) that combines
[Raylib](https://raylib.com) with dyibicc, and bundles
[Neovim](https://neovim.io)[^2]. Raylib is a programmer-centric
game/graphics library, in that there's no level-editor-type thing,
there's just a big header of useful functions that you write code
against.

The test shell (Rdy) starts by creating a top-level window via Raylib.
It first does a full compile of all the files in the project, and then
hooks up to the Neovim instance via RPC, which has been launched with
the project's C files.

Because they're connected over RPC, all buffer changes can be sent
directly to the compiler over RPC and there's no need to even write
files to disk. I actually started with normal file editing, and then
having the shell watch for updates. But it was a bit tedious to have to
constantly `:wa`. There's also a lot of messy states that files can be
in while the editor is (re)writing them: non-existent, zero bytes,
locked, etc. so RPC avoids all that.

Every frame, the shell just services RPC to get updates to pass to the
embedded compiler, starts drawing, calls the dyibicc C code entry point
(if there wasn't a compile error), and then page flips and repeats. It
feels **pretty slick** when the running C code continuously matches
what's in the editor.

The question that then comes up is: **What does it really mean to do a
"live update" of C code?**

It seems clear that when you change a function, you want the new one to
be linked in, and further, that you want all callers that were calling
the old implementation of the function to now call the new one. (You can
sort of imagine where you might not want that, but I think it would get
too confusing even if it were to be supported.)

Things in the data segment get less clear. If data segment values were
reinitialized, then you'd effectively be restarting the program, so it
seems that you mostly don't want that.

But! You do also want to be able to tweak e.g. string constants, so
things in `.rodata`/`.rdata` need to be updated to their new values.
This wasn't entirely obvious, as `dyibicc` inherited `chibicc`'s lack of
distinguishing `.rodata` data from `.data` data. They're somewhat
teased apart now, but there's likely more to do there.

It becomes fuzzy and requires understanding user-intent if you e.g. have
an array of function pointers that's globally initialized. Specifically,
a reference from `.data` into `.text`, or to put it another way from
"variable" into "constant". In the current implementation, those will
not update properly. When a new implementation of a function is linked
in, and the old one removed, the new function will be at a different
address. But the random `void*` stashed away in an array no longer has
any real association with that function (at least by name) so the array
will end up forever pointing to the first implementation of the
function.

We could try keeping old function addresses around and patch them to
start with a `jmp` to the new implementation, but I don't love the
never-garbage-collected aspect of that. There's no technical reason why
it's any harder to update the array of function pointers, so I think the
simplest solution would be to require an attribute/pragma on the object
to indicate to the runtime that it should be refreshed. `const` might be
enough of a "tag" in some cases too.

In summary, when relinking: Constants change, variables don't. Which
sounds funny out loud, but I think it makes sense.

## An unscripted demo

That wall of text doesn't really make it seem that cool, but it kind of
is! I thought I would try to record a short-but-captivating video,
because seeing it update in real time is the neat thing.

But as I'm lacking **Streamer Star Charisma** and snazzy video
production, we instead have to settle for a video of me mumbling, while
typing slowly and making typos, discovering bugs, and forgetting what I
was going to talk about. But maybe you can kind of see what's going on
and how it could be neat.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Di-GK1RkYh8?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

(You'll need to open it on YT and make sure it's set to 1080p and
fullscreen or you're definitely not going to be able to see what's going
on.)

---

[^1]: And even while printing lots of unnecessary console spam! hashtag always annoying

[^2]: Going straight to `vi` for the IDE strenously avoids popularity!
