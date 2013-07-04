---
layout: post
title: Copying syntax highlighted code from Vim
---

Occasionally, I need to email code to a co-worker, and in general,
Outlook seems to enjoy destroying anything you write in its editor.

It always wants to convert '-' to an endash, '--' to an emdash, replaces
quotes with smart quotes, capitalizes random words, and so on. Those are
great things for your average dude writing some English, but man does it
suck for programmers. It's terrible for command lines too.

If the code's longer than about a line, it's also pretty irritating when
you copy code from Vim, paste into Outlook, and you get plaintext. Some
people might prefer it that way, but everyone in my office uses rtf/html
formatted emails anyway, so I figured I might as well get some benefit
out of it at least.

I whacked up a Vim script "cliphtml" that copies from Vim, using your
current colorscheme and stuffs it in the clipboard in html format.
Current requirements are Windows, Vim with +python, and pywin32
installed in your system python. Windows Vim loads the python dll from
the system location (rather than statically linking unfortunately) so
you will have to install python2.4 (at least for Vim 7.2) and pywin32 if
you're not already using Python in your Vim.

To install the script, just save [cliphtml.vim](/images/cliphtml.vim) to
your plugins directory. The command is

    :ClipHtml

and then paste into Outlook. You should get something like this:

![Pasted into Outlook](/images/cliphtml_pasted.png)

It also works with ranges or visual ranges of course, so you can select
with 'V' and then :ClipHtml a snippet.
