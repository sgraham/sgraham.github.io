---
layout: post
title: Windows iTunes
---

I genuinely don&#8217;t understand.

I&#8217;m not trying to be difficult. I really tried to use iTunes this time.
It seemed like the march of inevitability if I wanted to get iPhone apps, and
I thought perhaps it would be nice to use. I grabbed the new 7.7 that has
iPhone apps, since I wanted to have a look at what was available. It was a
little large at 60meg, but hey, whatever, there&#8217;s lots of bandwidth to
go around these days.

First of all, I had to **reboot** after installing it. Insane. Strike one. If
that was it, well fine. But it&#8217;s ***completely*** unusably slow
on my laptop. The laptop is about 2 years old. It was Dell&#8217;s
top-of-the-line (XPS M170) when I bought it, so it&#8217;s not crazy fast, but
it&#8217;s not so slow either. I&#8217;m pretty sure that it&#8217;s still
well above the current median machine in performance.

I added my music collection (largely stored on a network drive). It&#8217;s
about 65 gig, comprised mostly of mp3s and flacs, both ripped from CDs and
downloaded. Maybe a little larger than some collections, but certainly not
unreasonably large.

I started the &#8220;Import&#8221; last night around 8pm. It&#8217;s now 2pm
the next day, and it&#8217;s still trying to download album artwork.
That&#8217;d be fine, except that apparently while it&#8217;s doing that,
it&#8217;s impossible for the UI to be responsive. WTF! *Is this goddamn
amateur hour?* It only refreshes the UI at the end of each attempt to download
an album cover?!

Pausing or unpausing music, or changing the volume (since apparently it feels
the need to steal the functionality of the hardware media keys) takes over 10
seconds. That is not hyperbole! It actually takes longer than 10 seconds for
anything to happen. On top of that, the mouse event handling also appears to
be &#8220;sampling&#8221; rather than using the event queue properly, because
if I just click the play/pause button nothing happens. I have to ***hold the
fucking mouse button down*** until the UI responds (10 to 15 seconds,
remember!), putting the button into the down state, and then release it.

On a side note, iTunes.exe currently owns roughly 300 threads, and has had a
continuous IO delta of around 500k/sec for nearly 24 hours now. Jumped up
Jesus Christ. You&#8217;re not controlling air traffic, you&#8217;re
cataloging and playing some fucking music.

If this is Apple&#8217;s shitty attempt to create some sort of Mac
&#8220;halo&#8221;, they&#8217;ve failed miserably. With 100% certainty, I
will never, ever, by a Mac with this as the demo of the user
experience.
