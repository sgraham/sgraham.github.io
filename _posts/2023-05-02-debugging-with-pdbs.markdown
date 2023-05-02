---
layout: newpost
title: Debugging with PDBs
---

I took a slight detour on the C JIT. I had specifically said before that I
didn't want to bother going to all the work of creating a standard
debugger for dyibicc, mostly because it was a big job.

But then debugging some long-tail and surely-still-more-to-come
[codegen](https://github.com/sgraham/dyibicc/commit/4df35f2207cf898ccd3ba2c9102a0d922d956ad8)
[bugs](https://github.com/sgraham/dyibicc/commit/78e9a78d40272f415fe435b608335f0a9830cf45)
I had the idea that it would be nice if I could see which source lines
were contributing to which machine code.

For a while, I'd been inserting blocks of `nop`s to delimit lines, and
that kind of works, but I kept thinking: "Sure, I don't need a full
debugging experience, but how hard could it be just to have the mapping
back to the source files?"

Which lead to me somehow nerd-sniping myself into a week of banging
away, and [2000 lines of
code](https://github.com/sgraham/dyibicc/commit/21dbc7d2225dcb583a0e8e38e0e184072fe751d4#diff-abdc0daa632d8a067244b2bb49d3b5ebf8473e8bec70a44a89ab8d2aae07fac2).

## Demo

So as to not bury the lede, here's a short demo of `dyn_basic_pdb`,
which is the header-library I've landed on to write pdbs.

<iframe width="560" height="315" src="https://www.youtube.com/embed/uGjJAxcU--Y?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The code is in
[dyn_basic_pdb.h](https://github.com/sgraham/dyibicc/blob/main/src/dyn_basic_pdb.h)
and there's a small [example of
usage](https://github.com/sgraham/dyibicc/tree/main/src/dbp_example) if
for some reason you want to do this very strangely specific thing
yourself too.

## Details

### Writing

I found `.pdb` quite a challenging a challenging format to write.

The [microsoft-pdb](https://github.com/microsoft/microsoft-pdb) repo
released a while back is what made it possible for anyone outside
Microsoft to have much chance of writing a useful pdb at all. This was
released at the request of the LLVM Windows team at Google, and thanks
to a lot of work, LLVM/Clang/LLD is also very good at writing pdb files.

The difficulty with writing one yourself is partly that there's limited
documentation (though LLVM has made a good start). Mostly though, it's
just that the format is old and complicated, and not really designed as
a file format. Think back before Windows 7, before Windows XP, before
Windows 95 to `segment:offset`, to the hazy days of 16 bit sizes, to the
era when people believed that "everything is a beautiful IDL interface
and disk formats are merely the persisted form of a COM blah blah". So,
e.g. there are now-dead (32 bit sized) pointer fields on disk that are
totally unnecessary. And hash table probing and bucketing strategies
have to match precisely (more on that later). And many other too deep in
the weeds details to even mention.

[LLVM's PDB documentation](https://llvm.org/docs/PDB/index.html) gives a
good high-level overview of the format, and how it's structured as a
paged-block format, as well as details on some of the streams that are
contained.

A quick summary is that the pdb file is more like a file system than a
normal file. A pdb is a set of streams of information, and streams are
written in non-contiguous chunks by page[^1] allocation. So each stream
is made up of a set of pages scattered throughout the file. There's also
support for atomic commit/rollback by having an A/B page map.

The container is relatively straightforward, but once you get into the
details of the individual streams it gets pretty intricate.

I'm not going to try to expand on LLVM's documentation here, but if you
look at `dbp_ready_to_execute()` in the header, you could in theory (?)
get some idea of how the streams fit together. It's not simple, but it
might be easier to use as a reference alongside LLVM, if only because
it's in a single file, rather than a large fully-featured reader/writer.
LLVM's implementation
[here](https://github.com/llvm/llvm-project/tree/main/llvm/lib/DebugInfo/PDB)
and
[here](https://github.com/llvm/llvm-project/tree/main/llvm/lib/DebugInfo/PDB/Native)
are definitely helpful though.

Having said that, here are a few things that stumped me for a while
and/or were slightly interesting.

#### NMT

The [Name Map
Table](https://github.com/microsoft/microsoft-pdb/blob/master/PDB/include/nmt.h)
is a string interning table that's used in a few places. I think it's
probably one of the better designed parts of the format (allegedly
thanks to a certain [Rico and
Richard](https://github.com/microsoft/microsoft-pdb/blob/805655a28bd8198004be2ac27e6e0290121a5e89/PDB/include/nmt.h#L24)
🙂!)

There's two parallel arrays, one that stores `\0` separated strings, and
one that stores by hash index the offset into the first array.

The tricky part here though is that it wasn't really intended as a file
format that others might read and write. So when the hash table is
serialized, you have to be sure that: 1) you're using the identical hash
function and probing method; and 2) use the exact same growth factor
calculations when the hash table part has to grow.

Some (most) readers don't rehash on load, they read the whole blob of
hash buckets in, and use it as-is. That means that when a reader hashes
"xyz" with their predetermined hash function, and decides that belongs
in bucket `N`, you'd better have already put it in bucket `N`, or it
just won't be found.

It would be easy enough in a new reader (or format) to simply load the
strings and then hash and store the map in whatever associative
container you wanted, but we're back here in the mid 90's, so... just
don't mess up, ok!?

Also, don't fall into the trap of believing that you wrote a hash table
in one location in this file, so surely the other map of strings to ints
is in the same format. The "Name Map Table" is in this format, but the
"Named Stream Map" which gives names to streams (ints) is stored in a
different format.

#### llvm-pdbutil vs. Dia2Dump/VS

Not a huge surprise, but one thing to be aware of is that there's some
room for intepretation in what should be acceptable. Since we want to
load pdb files in Visual Studio that's the final judge of what's
acceptable by definition, but it can definitely be helpful to use other
readers (like `llvm-pdbutil`) from the command line when testing. While
it tries to do some validation of things like missing parts or
unaligned pieces, there were a number of times where the `llvm-pdbutil`
dump appeared correct but `Dia2Dump` would just show no data.

So when you make a change, be sure to test with multiple readers.

#### SectionMapHeader

This is a very arbitrary detail, but I spent far too long debugging
before I realized that the `SectionMapHeader` (which is itself a
substream of the `DBI` stream) apparently needs to have [at least two
entries](https://github.com/sgraham/dyibicc/commit/273bcc76c8a4e1b0953d09d089ddf49bd064842b#diff-abdc0daa632d8a067244b2bb49d3b5ebf8473e8bec70a44a89ab8d2aae07fac2R857).
It's not entirely clear (to me) what the Section Map Header is even
accomplishing, but in my JIT's code at that point there was only a
single code section, so I naively thought I would just put a single
section in the Section Map.

But **nope**, that apparently causes all symbols and line mappings to have
an invalid RVA when read by the DIA SDK, which in turns means that none
of them are found.

So, work in very small increments, and be sure again to test with
multiple readers all the time.

### Loading

Once you finally get a working `.pdb`, you just pop over to Visual
Studio or WinDBG and say, umm, er....

There's no way to directly load a .pdb as it sort of doesn't make sense.
There has to be a block of mapped-into-memory code associated with it.
So in addition to writing a `.pdb`, the library also has to write a
`.dll`. This DLL has an `IMAGE_DEBUG_DIRECTORY` entry that points at the
`.pdb`. That way, when you call Win32 `LoadLibrary()` (and slam your
actual JIT'd code on top of the address space where the `.dll` was
loaded), Visual Studio will see the pointer to the .pdb, load it[^2],
and you'll be able to debug as usual. This doesn't seem too complicated,
but there were (naturally) some gotchas.

I had originally intended to allow the user to own the main
`VirtualAlloc()` of code space. That way, they could generate code as
usual, and then optionally generate a `.pdb` if they were debugging.
Unfortunately, I don't think it's possible to have code at offset (RVA)
zero of a DLL. So if the user generates code right at the first byte of
the memory they allocated, then when the fake DLL gets loaded to that
location, the RVA of `.text` has to be past the normal DLL file header,
typically at `0x1000`. One workaround would just be to say that the user
has to "give" us the first 4096 bytes of the mapping. I decided instead
to have the library allocate the memory for you (so it can add the extra
space), and so you can either use that allocation if you're debugging,
or use `VirtualAlloc()` yourself if not.

Another gotcha is not really related to PDB files, but is related to
JITs more generally, and that's the need to provide `.pdata` and
`.xdata` to Windows for it to do stack traces. There's a bytecode in
every x64 .exe/dll that describes what the prolog of a function does to
the stack, and so how it can be unwound. This is used for stack walking
on x64, and for structured exception handling. This is all [pretty
well](https://learn.microsoft.com/en-us/cpp/build/prolog-and-epilog?view=msvc-170)
[documented](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64?view=msvc-170)
if a little complex. Normally for a JIT, [you use
`RtlAddFunctionTable()`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtladdfunctiontable)
which provides the same prolog bytecode information at runtime. I
assumed I could still do this, so the pdb library wouldn't need to have
anything to do with `.pdata`.

However! There's one undocumented assumption which is that ranges that
are statically mapped to a PE **only** use the `.pdata` that's in the
exe, and silently ignore any data provided by `RtlAddFunctionTable()`.
Because of our hack to use `LoadLibrary()` to load a dll which in turn
references that pdb that we want to load, this situation applies to us.
So, the "empty" DLL is no longer be entirely empty, it actually contains
just the `.pdata` and `UNWIND_INFO` structures that are otherwise
uninteresting to us. But once that's in place, we get proper stack
traces and things work as expected.

### Coda

I'm not sure how useful this functionality will end up being for me, but
it was an interesting spelunking challenge.

Maybe someone else will find it useful as a library or as reference, as
while there's a number of decent quality source-available readers that
people mentioned to me on Mastodon and Twitter e.g.
[raw_pdb](https://github.com/MolecularMatters/raw_pdb) and Rust's [pdb
crate](https://docs.rs/pdb/latest/pdb/), I don't know of any writers
other than LLVM and Microsoft's code dump (though that doesn't even come
close to compiling).

I don't think I'm likely to extend it to including `TPI` and `IPI`
streams (those contain variable and type information) just because it's
a lot more work, so it's sort of "done" for now. Of course, I said that
about debugging in general too, so who knows.

---

[^1]: Typically 4k large on any new-ish pdbs.

[^2]: I saw "helpful" errors like these a **lot** ![unspecified error](/images/unspecified_error.png) ![Bad image](/images/bad_dll_image.png) Or Dia2Dump/llvm-pdbutil would just crash with no output. Good pdb vs bad pdb? No crash vs crash! Easy to debug.
