---
layout: post
title: Android ADT + eclim on Ubuntu 9.10
---

Stuffing this here so I remember for next time and for search engine
stumblers...

On Ubuntu (9.10) I installed Eclipse (3.5) via apt-get, then the Android
ADT per Google instructions, and then eclim via `sudo ./eclim_1.5.6.sh`.
After installing eclim, the Android functionality in Eclipse
disappeared.

I'm not sure what happened, the Android software was still listed as
being installed, but the functionality just didn't seem to be available.

If instead I just install eclim into local user i.e. `./eclim_1.5.6.sh`,
all seems well.

If you got yourself into the same situation, the easiest thing I found
to do was to "Completely Remove" eclipse  and related packages via
Synaptic, then `sudo rm -rf /usr/lib/eclipse` and `sudo rm -rf
~/.vim/eclim` (or wherever you have your vimfiles), and then install
again, making sure not to install eclim as root.

As a side note, I didn't know about [eclim](http://www.eclim.org/) until
the other day. It seems pretty sweet. You can run Eclipse headless (or
not) and then most/all your project maintainance and editing in the
sanity and comfort of Vim. Specifically, this includes proper completion
via `^X^U` (`imap`d to something nicer, natch) as well as error
annotations on write.
