import hashlib
import imaplib
import os
import secrets
import smtplib
from email.message import EmailMessage


def generate_confirmation_code():
    while True:
        confirmation_code = secrets.randbelow(1_000_000)
        if confirmation_code > 100_000:
            return confirmation_code


def fetch_massage():
    # fetch confirmation code from aix finance email

    email_addr = 'finance.aixpro.gmail.com'
    password = 'password'
    server = 'imap.gmail.com'

    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_addr, password)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []
    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email_addr.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')


def send_code(email_addr):

    code = generate_confirmation_code()
    message = f'Hello there. Here is your confirmation code: {code} Please enter it continue signing in. Do not share it with anyone.'
    email_id = 'finance.aixpro@gmail.com'
    email_pass = 'scco mazj fwln uxyd'
    msg = EmailMessage()
    msg['Subject'] = 'Xfinance Confirmation Code'
    msg['From'] = email_id
    msg['To'] = email_addr
    msg.set_content(message)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)
        smtp.quit()

    if os.getcwd() != '/home/iceman/Desktop/xfinance/.xf-data':
        os.chdir('/home/iceman/Desktop/xfinance/.xf-data')

    confirmation_code_hash = hashlib.sha256(bytes(str(code), 'utf-8')).hexdigest()
    with open('stored_confirmation_code_hash', 'w') as confirmation_code_hash_file:
        confirmation_code_hash_file.write(confirmation_code_hash)

