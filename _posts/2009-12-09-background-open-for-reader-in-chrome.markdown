---
layout: post
---

Chrome just learned how to do
[extensions](https://chrome.google.com/extensions/) thankfully.

I was already using Chrome as my main browser, mostly because it's all-around
smokin' fast. There's minor irritations, but the Chrome team sticks to a
minimalistic and sleek world view, so the toggles I'm looking for are never
going to show up as mainline options.

In addition to adding buttons and processing to Chrome, the extensions layer
enables Greasemonkey-ish "content scripts". In Google Reader, the default
behaviour for the 'V' shortcut key is to open the RSS item in a new tab.
Unfortunately, it opens it in a foreground tab rather than a background tab.

I like to burn through all the unread items, V-ing the ones that seem
interesting, and then later go back and read all of them. This is quite cumbersome
in Chrome when combined with non-MRU tab switching behaviour, and tab pinning.
When Reader is pinned on the left, the number of keystrokes to get back to
Reader isn't "one", and it isn't even constant. So, you end up needing to grab
the mouse to get back, which is irritating.

So!

I made an [extension for Chrome that adds "Shift-V" to Reader that opens the
selected item in a background
tab](https://chrome.google.com/extensions/detail/mhlmdgjoakcfdigjjlmonhjphchebcjm).

A couple slight hacks:

- Shift-V instead of V: unfortunately, there doesn't appear to be a way to
  stop propagation of the event to Reader in the API exposed to extensions
  yet, so the background open can't replace the default open. Instead it has
  to go on a different key binding. Occasionally, I do actually want to read
  the item right away though, so I guess it handles that case. (I'd actually
  rather that they were swapped so that foreground open was Shift-V, but
  anyway...)
- The `chrome.tabs.create` API doesn't have an option to open the tab in the
  background, so instead I have to save the current (Reader) tab, open the new
  tab, and then switch back to the Reader tab. On some machines (versions of
  Chrome?) this causes a visible flicker, but on the current as of
  right-this-minute, it doesn't seem to, so it'll do for now.

Yes, I've spent longer API spelunking and writing this post than I ever would
have spent doing Ctrl-Shift-Tab/Ctrl-PgDn.

But, it's just one of those things that reduces friction and irritation and
makes me happy. Or at least sates the OCD beast for a while.
