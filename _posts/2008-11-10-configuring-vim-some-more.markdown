---
layout: post
---

As an addendum to <a
href="http://items.sjbach.com/319/configuring-vim-right">http://items.sjbach.com/319/configuring-vim-right</a>

Here's a few more that I think are un-live-able-without:

{% highlight vim %}
" ease of use keyboard mappings (why do I care about top/bottom of screen?)
map H ^
map L $

" buffer switching/management, might as well use those keys for something useful
map <Right> :bnext<CR>
imap <Right> <ESC>:bnext<CR>
map <Left> :bprev<CR>
imap <Left> <ESC>:bprev<CR>
map <Del> :bd<CR>

" get rid of stupid scrollbar/menu/tabs/etc
set guioptions=a

" don't need /g after :s or :g
set gdefault

" i prefer this to visualbell
set noerrorbells

" Hide the mouse pointer while typing
set mousehide
{% endhighlight %}

I've used all of these for longer than I can remember, probably time to troll
through recent help files and vim.org to find new and exciting juicy
settings.

EDIT: forgot the one I miss the most when I don't have my .vimrc:

{% highlight vim %}
cab o find
{% endhighlight %}

so that :o does something useful. I'd like one of the emacs-style
smart-fuzz-file-opener command line thing, I should probably hunt around for a
plugin to do that.
