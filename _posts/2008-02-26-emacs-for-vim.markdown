---
layout: post
---

I&#8217;m having a whack at trying to learn a reasonable amount of Emacs so I can attempt a project more reasonably in sbcl (and Weblocks). I&#8217;ve been programming in Vim for about 12 years and my brain/hands are very, very angry at this editor transgression.

Mostly because I know I&#8217;ll give up, and then try again much later, here&#8217;s some stuff that is permanently ingrained in my Vim brain that is the closest I could find in Emacs (so far at least). To be edited as I find more things. Vim on the left, Emacs on the right:

### Movement
* C-f, C-b = C-v, M-v
* hjkl = C-b, C-n, C-p, C-f 
* HL (or ^$ for most people) = C-a, C-e
* wb = M-f, M-b
* O, o = ? (C-o does some stupid thing)
* u, C-r = ?

### Change/Deleting
* das = ?
* cab = ?
* gqap = ?
* dd = ?

### Clipboard
* "+y = ?
* "+P = ? 

The page movement commands are probably my biggest problem right now: for one they&#8217;re the dumb ones like Vim&#8217;s C-u/C-d that only move half a page (haven&#8217;t figured out how to make them only leave one line instead yet), and for two, it&#8217;s just kind of painful because you have to move your pinky and then repress the v, rather than just hold down control and toggle between f/b. Anyway, whatever. I&#8217;ll suck and use PgUp/PgDn for now.

No hjkl of course kills me, but everyone else too.

I keep hitting Esc when I&#8217;m done entering text so then the next Ctrl/Meta command doesn&#8217;t work because it&#8217;s been prefixed by an Escape. Ack. Pffft.

The most amusing thing so far is that I couldn&#8217;t figure out enough to edit my .emacs in Emacs so the first few edits were:

    $ vim ~/.emacs

Hrm.
