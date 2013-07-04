---
layout: post
title: Hackage for Android and Vonage voicemail .wav's
---

Froyo (Android 2.2)
[broke](http://code.google.com/p/android/issues/detail?id=8730) the
playing of Vonage's attached voicemails. I think it's because
they're not really .wav's or something, but whatever the reason,
it's a total pain in the ass.

Presumably it'll be fixed in Gingerbread, but it was driving me crazy in
the meantime.

I hacked together some of the worst code ever. I honestly felt like I
was programming like an AI would: Google for something, paste it, run
it, *then* read it to see why it didn't work, and repeat.

Anyway, it took me almost an hour, so here it is case it helps someone else.

Put it in [`wavconv.py`](/images/wavconv.py) (or whatever) and run it as:

    python wavconv.py your_user_id@gmail.com your_gmail_password

It uses `sox` to convert the wav's to .ogg which seem to play OK on my
Nexus One. To install sox on Ubuntu, just do:

    sudo apt-get install sox

Please feel free to leave a comment if you know how to do it for another
platform.

It sits in a loop and checks for messages every 2 minutes, converting
them if it sees a new one. So, you'll probably want to run it on a
server in a `screen` session. Or maybe it'd be better in cron and delete
the loop/sleep.

Contents of the above link, below.

{% highlight python %}

import email, getpass, imaplib, os, smtplib, sys, time
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
from email import Encoders

if len(sys.argv) != 3:
    print "usage: wavconv.py user@gmail.com your_password"
    raise SystemExit()

user = sys.argv[1]
passwd = sys.argv[2]

while True:
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user, passwd)
    m.select("INBOX")

    resp, items = m.search(None, "(SUBJECT \"new voicemail\")")
    items = items[0].split()

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)

        if mail.get_content_maintype() != 'multipart':
            continue

        #print "["+mail["From"]+"]: " + mail["Subject"]

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            if part["Content-Transfer-Encoding"] != "base64":
                continue

            filename = mail["Date"]
            filename = filename.replace(" ", "_").replace(":", "_").replace(",", "_")
            # hacky non-dupe!
            if os.path.exists(filename) or mail["From"] == user:
                break

            fp = open(filename, "wb")
            fp.write(part.get_payload(decode=True))
            fp.close()
            os.system("sox " + filename + " conv.ogg")

            # build a response and send it (ugh!)
            msg = MIMEMultipart()
            msg['Subject'] = mail["From"] + ", " + mail["Subject"]
            msg['From'] = user
            msg['To'] = user
            attach = MIMEBase('audio', 'ogg')
            part.set_payload(open("conv.ogg", 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="conv.ogg"')
            fp.close()
            msg.attach(part)

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(user, passwd)
            s.sendmail(msg["From"], [msg["To"]], msg.as_string())
            s.quit()

            print "converted", filename

    time.sleep(120)

{% endhighlight %}

