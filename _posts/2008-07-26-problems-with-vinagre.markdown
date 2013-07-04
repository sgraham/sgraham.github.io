---
layout: post
---

So, the default remote desktop app in Ubuntu changed from, um, I don&#8217;t
know what actually, to a new app called &#8220;Vinagre&#8221;.

You&#8217;d think that&#8217;d be something I wouldn&#8217;t give a patooty
about. The first thing you notice is that it has a list on the side that lets
you keep track of servers you connect to which seemed nice enough.

I didn&#8217;t use it much at first, so I thought nothing more about it.

Today, I started using it. Dear god:

* Tried to connect to a fully up-to-date Fedora box (from a fully up-to-date
  Ubuntu). vino-server crashes on the Fedora machine. I don&#8217;t know
  who&#8217;s fault it is, but I don&#8217;t really care. Working around that
  by using XDMCP for the time being, but that&#8217;s pretty irritating,
  interface-wise.
* While repeatedly trying to connect to the Fedora box (it silently fails on
  the Ubuntu machine), Vinagre doesn&#8217;t save the last-entered machine
  name, so I have to keep entering &#8220;192.168.0&#8230;.&#8221; every time.
  Irritating.
* Insanely hard to send Ctrl-Alt-Del to log into Windows machines. For same
  reason, Ctrl-Alt was chosen as the &#8220;Capture/Release&#8221; input. So,
  in order to send Ctrl-Alt-Del to login to a Windows box, you have to first
  focus the Viagre app (click/whatever), then make sure you&#8217;ve
  ***uncaptured*** the input by doing Ctrl-Alt, then finally, ***recapture***
  the input by doing Ctrl-Alt again, and ***then without letting go*** of
  Ctrl-Alt, press Del to get the final combo. If you just push that combo of
  course, the Ctrl-Alt first removes capture, and then sends Ctrl-Alt-Del to
  the local machine. Not very intuitive, especially since there&#8217;s very
  little (no?) indication of whether input is captured.
* Related, there seems to be absolutely no way to send F11 to the client
  machine. The general hotkey behaviour is irritating enough as it is: Alt-F4
  closes either all of Vinagre, or an app on the client, depending on whether
  you&#8217;ve pressed Ctrl-Alt recently, with no indication of which
  &#8220;mode&#8221; you&#8217;re in). But, it seems that F11 is even worse.
  If you&#8217;re in captured mode, then most things seem to be sent to the
  target machien, but apparently F11 was deemed too important to be handled
  normally, and there&#8217;s no configuration mechanism. Fine, until I try to
  debug something and naturally hit F11 to &#8220;Step Into&#8221; a function.

**Update** When input is captured, there&#8217;s no way to scroll the virtual
desktop if it&#8217;s bigger than your current monitor. WTF?

Basically, it just seems like this app was pushed out way too quick to the
main/default user stream. Please give me back my old VNC/RDP viewer. :(

