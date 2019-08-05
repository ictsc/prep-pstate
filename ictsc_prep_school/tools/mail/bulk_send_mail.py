#!/usr/bin/env python2
# coding: utf-8

import os
import sys
import mimetypes
import time
# py2じゃないと動かない
import smtplib
import yaml
import dotenv
from email import encoders
from email.utils import formatdate
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

# smtp settings
SMTP_HOST = 'puresuta.sakura.ne.jp'
SMTP_PORT = 587
SMTP_ACCOUNT = 'ICTSC2018予選 <yosen@icttoracon.net>'
SMTP_USERNAME = 'yosen@icttoracon.net'
# infra password
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD').encode('ascii')

dry_run = False if len(sys.argv) > 3 and 'send' == sys.argv[3] else True

# login
if not dry_run:
    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)

def create_message(to, subject, message, filepath=None):
    msg = MIMEMultipart()
    msg["Subject"] = Header(subject, 'utf-8')
    msg["From"] = SMTP_ACCOUNT
    msg["To"] = to
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    if filepath is not None:
        filepath = filepath.encode('utf-8')
        attach_file(msg, filepath)
    return msg

def attach_file(msg, filepath):
    print(filepath)
    if not os.path.isfile(filepath):
        print('invalid filepath')
        sys.exit(1)

    # Guess the content type based on the file's extension.
    # Encoding will be ignored, although we should check for simple things like gzip'd or compressed files.
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(filepath) as fp:
            # Note: we should handle calculating the charset
            item = MIMEText(fp.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            item = MIMEImage(fp.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filepath, 'rb') as fp:
            item = MIMEAudio(fp.read(), _subtype=subtype)
    else:
        with open(filepath, 'rb') as fp:
            item = MIMEBase(maintype, subtype)
            item.set_payload(fp.read())
        # Encode the payload using Base64
        encoders.encode_base64(item)

    # Set the filename parameter
    item.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
    msg.attach(item)

# read yml
data = yaml.load(open(sys.argv[1]))

if not dry_run:
    res = raw_input('are you sure to send email?[YES/no]').strip()
    if res != 'YES':
        sys.exit(1)

# send mail
for mtype in data['teams']:
    for team in data['teams'][mtype]:
        subject = data['template'][mtype]['subject']
        msg = data['template'][mtype]['message'].format(**team)
        filepath = team.get('filepath')
        message = create_message(team['email'], subject, msg.encode('utf-8'), filepath)
        print u'sending to: {}<{}>'.format(team['email'], team['name'])
        if not dry_run:
            result = smtp.sendmail(SMTP_ACCOUNT, team['email'], message.as_string())
            print(result)
            time.sleep(4)
        else:
            print message.as_string()

if not dry_run:
    smtp.quit()
