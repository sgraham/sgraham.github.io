---
layout: post
title: Replacing the input reader in cmd.exe
---

In my [ongoing](/2013/07/04/git-branch-in-cmd/)
[attack](/2013/07/21/suppress-terminate-batch-job/) on cmd.exe, the next thing
I wanted to have was tab-completion of git branch names, since I have
apparently no memory for remembering what the heck I called
_that-other-branch-where-I-was-doing-that-thing_.

There's a somewhat complicated interaction between what's strictly cmd, and
what's in the `csrss` process that's theoretically available to all console
programs ("doskey" handling). Because the reading of an input line is handled
in a blocking function that escapes back to cmd when it wants completion, I
thought it might be possible to just hook in and replace that. Unfortunately it
got a bit messy because of the internal state maintained by cmd for the
contents of the line, where it is in the line, and so on.

So instead, I decided to full-on replace the implementation of `ReadConsole` in
cmd. The drawback of this approach is that I have to implement all input
handling. This of course is also the benefit, as I can control and do whatever
I want inside there now.

`ReadConsole` gets patched in the same way as the previous ones (IAT patching),
and then it's "just" a matter of writing readline-ish code to implement all the
various line editing functionality.

First, there's all the basics of typing, Home, End, Ctrl-Left/Right to jump by
words. And, command history with Up/Down. Tab does basic file completion, etc.

But then, I added a bunch more convenient functionality like saving command
history across sessions. This required replacing `msvcrt!exit` which is when
this history is saved.

And I got to add some bonus keybindings:

- Alt-Up is the same as "cd .."
- Alt-Left/Right (or the browser navigation keys) move through previously
  visited directories web browser-style.
- Ctrl-W kills back a word, Ctrl-Backspace kills back a path component.
- Ctrl-L clears the screen, maintaining the current command.
- Ctrl-Enter opens an Explorer window to the current directory.
- Ctrl-A and Ctrl-E do the same as Home and End.
- Ctrl-K or Ctrl-End delete to the end of line.
- Ctrl-U or Ctrl-Home delete to the beginning of the line.

And most importantly, tab completion is improved. This is still nascent, but is
already much improved over cmd's native completion. There's command-in-path
completion, so if you're at the beginning of a line, the PATH (and built-in cmd
functions) will be offered for completion, rather than random files in the
current directory. There's some built in support for git completion too, so for
example:

    C:\>git ch<TAB>

cycles through

    C:\>git checkout
    C:\>git cherry-pick

And

    C:\>git checkout -<TAB>

cycles through

    C:\>git checkout --quiet
    C:\>git checkout --ours

etc. And finally, branches:

    [master]C:\src\cmdEx>git checkout o<TAB>

completes through:

    [master]C:\src\cmdEx>git checkout origin/HEAD
    [master]C:\src\cmdEx>git checkout origin/master

`checkout` is currently the only command that has its arguments understood, but
I'll fill out other commands over time as they seem useful.

If by some chance you are "User Number 2" (i.e.  not me) and you're having
problems with the new input handling, you can disable that part by `set
CMDEX_NOREADCONSOLE=1` (but keep, e.g. git branch name in prompt).

Code and prebuilt binary are at [github](https://github.com/sgraham/cmdEx/).
