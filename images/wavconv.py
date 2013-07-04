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
