---
layout: post
title: Gmail Backup via IMAP using offlineimap
---

Every so often I have a minor freakout when I realize the amount of data
that's stored in my Gmail account. The first thing I do is make my
Google account password longer and add more obscure characters. Then, I
feel slightly nervous that it's stored in the US and subject to
*who-knows-what* laws.

Once those feelings pass, I'm mostly concerned that due to &lt;unforseen
circumstance&gt; I might lose access to everything that's in there. It
would be a massive hassle.

Fortunately, Gmail supports IMAP access to the mail so it should be
relatively straightforward to back up everything. I finally got around
to doing that today. I ended up using "offlineimap" which does what its
name implies.

First, install offlineimap. On Ubuntu, this is just:

    sudo apt-get install offlineimap

If you know how for other OSs, please feel free to leave a comment.

Then, I made a configuration file that looks like this:

    {% highlight ini %}
    [general]
    accounts = Gmail
    maxsyncaccounts = 3

    [Account Gmail]
    localrepository = Local
    remoterepository = Remote

    [Repository Local]
    type = Maildir
    localfolders = /backup/USERNAME/mail

    [Repository Remote]
    type = IMAP
    remotehost = imap.gmail.com
    remoteuser = USERNAME@gmail.com
    remotepass = PASSWORD
    ssl = yes
    maxconnections = 1
    realdelete = no
    {% endhighlight %}

Of course, you'll need to replace "USERNAME", "PASSWORD", and probably
change "/backup/USERNAME/mail" to where you want the backup to live.

I saved this configuration into `/backup/USERNAME/USERNAME.imaprc`.

Then, try running it with:

    offlineimap -c USERNAME.imaprc -u Noninteractive.Basic

The `-c` argument points it at our config file rather than ~/.something
and `-u` changes the UI to a standard one rather than a heavy colourful
curses default (we're going to use it as a cron job in a second so we
want a log-style).

If that works, it will probably take a while, but all your mail should
get synced into that folder. You can confirm that everything worked by (e.g.)

    mutt -f /backup/USERNAME/mail/INBOX

which will use "mutt" to view the data saved there (you might need to do
`sudo apt-get install mutt` for that too). If you look in the `mail/`
directory, you should see all your labels, as well as the standard Gmail
ones. And, though the files in the directories have ugly names, each one
corresponds to one mail message stored in text format, so in case of
emergency you could always go grubbing through the files to find
important information.

Now, if everything looks OK, you'll probably want to schedule this to
run every so often. To accomplish this, I added this script into
`/etc/cron.daily`

    #/bin/sh
    offlineimap -c /backup/USERNAME/USERNAME.imaprc -u Noninteractive.Basic

Don't forget to `chmod +x` that script.

And now I can sleep a little easier. I'd still be a Sad Panda if Gmail
goes away, but I be much less irritated with a backup copy.

As you might glean from the name of the target directory (`/backup`)
this folder is also backed up via rsync. This is probably not necessary
(assuming both Gmail *and* your copy don't disappear at the same time)
but it was just as easy for me.

Another possibility might be to sync Gmail directly into a large Dropbox
folder. While it seems a little silly, it would then be almost
impossible to lose all the copies of your mail that would be scattered
around your various computers.
