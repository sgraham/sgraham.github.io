---
layout: post
title: bash .inputrc tab completion incantations
---

I can&#8217;t stand hitting TAB and having it do nothing because there&#8217;s
two matches. Cycling seems vastly more useful to me. And, history-search (F8
in Windows), but both directions using PgUp/PgDown. I can never remember this
magic so here it is for posterity (goes in ~/.inputrc):

    TAB: menu-complete
    "\e[Z": "\e-1\C-i"
    "\e[5~": history-search-backward
    "\e[6~": history-search-forward

Then, Tab and Shift-Tab cycle, and PgUp/PgDown cycle through history that
matches. Much better!
