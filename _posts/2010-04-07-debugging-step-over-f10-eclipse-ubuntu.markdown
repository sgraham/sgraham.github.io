---
layout: post
title: Step Over in Eclipse under Ubuntu using F10
---

And another for myself and search engine stumblers...

If you use Eclipse on Ubuntu coming from 15-20 years of Visual Studio
you'll soon be remapping the debugging shortcut keys to match Visual
Studio's before you start swearing up a storm.

However, F10 is mapped to `menubar_accel` by something in Ubuntu. Gnome?
Metacity? Not sure what exact thing it is that steals it, but the key
doesn't make it to Eclipse anyway, so pressing F10 just opens the `File`
menu in Eclipse which certainly isn't what you want.

### The fix

Run `gconf-editor`, browse to `/desktop/gnome/interface` then scroll
down to `menubar_accel` and delete the `F10` value.

You could probably reassign it instead, but if you're like me, you've
never used that functionality on purpose so don't bother.
