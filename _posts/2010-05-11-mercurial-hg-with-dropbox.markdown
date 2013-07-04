---
layout: post
title: Mercurial (hg) with Dropbox
---

I use Dropbox and Mercurial together so often now, and it's so freakin'
awesome.

But just as I was setting up another repo, I realized that there was a
slim possibility that there's programmers out there who don't use this
trick. So they're still doing something crazy for source control, like
trying to manage an SVN server, or a P4 server, or dealing with "only 1
private repo" restrictions, etc.

So... here it is, easy as pie. Or something that's easy, that isn't pie.
Your Mom, etc.

First, [sign up for
Dropbox](https://www.dropbox.com/referrals/NTMzMDU5Mzk). (That's a
referral link, you'll get an extra 250 meg on top of your free 2 gig if
you use that instead of just going to the website).

Now, use Mercurial as normal. [HgInit](http://hginit.com/01.html) is a
decent basic tutorial. You'll probably want to install hgtk on Linux, or
TortoiseHg on Windows. But, just for example, here's the command line
version:

    ~/myproj$ hg init
    ~/myproj$ hg addremove
    ~/myproj$ hg commit -m "initial commit"

Now you have revisions locally, which is nice enough, but that's just
Mercurial. If your hard drive dies, you're hooped.

On the other hand, you didn't have to worry about servers or making
depots, or backup, or other mucking around until you've spent at least a
few hours on the exciting new "myproj" and you decide you'd rather not
lose it.

So, what do you do? First, clone your repo into your Dropbox:

    ~$ cd ~/Dropbox
    ~/Dropbox$ hg clone ~/myproj ~/Dropbox/myproj-hg --noupdate

The syntax is `hg clone <from> <to>`. The `--noupdate` flag tell
Mercurial to just store the repository data, not to check out a working
copy. You're **never going to work directly in the Dropbox directory**,
but instead use it as a "remote" where you push and pull to and from it.
The only thing that will ever be in that directory is the `.hg`
directory, and there's no user-serviceable parts in that particular one.
That's why I renamed `myproj` to `myproj-hg` in the clone step, just so
I remember that it's a Mercurial directory, and it's supposed to be
"empty" (because the `.hg` will be hidden on Linux).

Second step, back in your original directory, edit your paths to point at
the Dropbox backup of your repository:

    $ vim ~/myproj/.hg/hgrc

(or your editor of course). Paste something like this (the file will be
new/empty if you haven't added anything else yourself:

    [paths]
    default = /home/sgraham/Dropbox/myproj-hg/

Replacing "sgraham" and "myproj" naturally. 

Now,

    $ hg push
    $ hg pull

will work as expected in `~/myproj`, and every time you push, you'll
have a secure, private, offsite backup of your code.

Step Three: Well, that's it. There's no more steps.


When you go to another machine, say a Windows machine, all you need to
do to get access to your repository is to install Dropbox and then clone
from it:

    C:\code> hg clone "C:\Users\sgraham\My Dropbox\myproj-hg" myproj

And that's it. `hg push` and `hg pull && hg update` will already work
properly.

And there you have it, Dropbox is the shizzle. Along with Mercurial,
you've got two great tastes that taste better together.
