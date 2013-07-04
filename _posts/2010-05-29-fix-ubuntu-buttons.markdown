---
layout: post
title: Fix Ubuntu 10.04 Lucid minimize/maximize/close button position
---

I [tweeted](http://twitter.com/sgraham_guid) this on first install, but
that's like throwing it into wind if you ever want to remember it (i.e.
when I install on a new PC).

This **leftist** conspiracy must be fought people! Here's the one liner
you're looking for:

    gconftool -s /apps/metacity/general/button_layout -t string "menu:minimize,maximize,close"

That is all. Fight The Power! Represent The People! Other Nonsensical
Slogan!
