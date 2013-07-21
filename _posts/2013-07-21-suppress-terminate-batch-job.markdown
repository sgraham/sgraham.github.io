---
layout: post
title: Suppress 'Terminate batch job (Y/N)?' in cmd.exe
---

In my [ongoing rewrite of cmd.exe from the
outside](/2013/07/04/git-branch-in-cmd/), my next target was the
extraordinarily aggravating prompt that cmd presents when you Ctrl-C
when running a batch file.

    c:\>type x.bat
    pause

    c:\>x

    c:\>pause
    Press any key to continue . . .           <- Press Ctrl-C here
    Terminate batch job (Y/N)?

Yup. I pressed Ctrl-C, I'm pretty sure I want to, you know, *interrupt*
things. It also isn't always enough to Ctrl-C again to get out, so you
actually have to press Y, Enter. And, you're in an indeterminate state
regardless of whether you respond Y or N, making it completely
pointless.

It's mainly annoying for a bunch of tools that wrap their main .exe in a
batch file. On Linux/Mac, there's no particular penalty to doing so, so
it's sometimes easier to have the real binary in a different folder and
have a forwarding script in the `PATH` that runs the binary.

So, I've probably hated that prompt for going on 20 years now. No
longer! Sunday July 21st, 2013 I took a stand. **NO MORE DUMB PROMPT**.

This one was implemented slightly differently than the previous git
branch functionality. The main difference is that the internal cmd
function `PromptUser` is used in a variety of places (for example, to
confirm deletion or overwrite of files), and, there's no obvious call to
an imported kernel32 function nearby that can be used to modify how it
works.

So, instead, I decided the best tactic was to find the appropriate call
to `PromptUser` in another internal function `CtrlCAbort`. It passes
what looks like the message id (to be looked up for localization) and
then does the appropriate batch terminating if `PromptUser` returns `1`.

The tricky part is that those functions are purely internal
implementation functions and aren't imported or exported. But {helpfully
| awesomely | regrettably}, Microsoft publishes PDBs for many Windows
system binaries, and an [API for downloading and
interpreting](http://msdn.microsoft.com/en-us/library/windows/desktop/ms679294.aspx)
those symbols.

With that in hand, it's a relatively straightforward matter of using
DbgHelp to find the location of `CtrlCAbort` in cmd (we're already
injected into the process), and then finding the call site that matches
the call to `PromptUser`, and patching it to emulate `PromptUser` having
returned `1`. The call site is quite distinctive because of the pushing
of the message id, so given the start address of the function there's
little likelihood of a false positive.

And just like that:

    c:\>c:\src\cmdEx\out\cmdEx.exe

    c:\>x

    c:\>pause
    Press any key to continue . . .           <- Press Ctrl-C here

    c:\>

Ahh, the sweet taste of victory.

Code is at [github](https://github.com/sgraham/cmdEx/).
