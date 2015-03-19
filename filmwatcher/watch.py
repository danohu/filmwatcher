#!/usr/bin/python3

import requests
import urllib.parse
from email.mime.text import MIMEText


SEARCHES = [
    'Rocky Horror',
    'Stilyagi',
    'Whiplash',
    'Liquid Sky',
    'A Dangerous Method',
    'Spirited Away',
    'Synecdoche',
    'Hurt Locker',
    'Monster',
    'Juno',
    'Almost Famous',
    ]


try:
    # my login details are hidden here
    # you'll probably want to adjust below instead
    from doh.private import mailserver, EMAIL_FROM, EMAIL_TO
except ImportError:
    EMAIL_FROM = 'from@example.com'
    EMAIL_TO = 'to@example.com'
    def mailserver():
        import smtplib
        server = smtplib.SMTP('host', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('user', 'password')
        return server


def is_showing(searchterm):
    url = 'http://www.zitty.de/list?type=cinema&q=%s' % urllib.parse.quote_plus(searchterm)
    result = requests.get(url).text
    notfound = 'Keine Ergebnisse zu Ihrer Suchanfrage gefunden' in result
    return not notfound



def check_all():
    for term in SEARCHES:
        if is_showing(term):
            yield term

def watchdog():
    found = list(check_all())
    if not found:
        return
    server = mailserver()
    body = '''
    The following films were found showing in Berlin:
    '''
    for f in found:
        body += '\n\t\t%s' % f
    mailtext = MIMEText(body)
    mailtext['To'] = EMAIL_TO
    mailtext['From'] = EMAIL_FROM
    mailtext['Subject'] = 'Films showing: %s' % ','.join(found)
    server.sendmail(EMAIL_FROM, EMAIL_TO, mailtext.as_string())

if __name__ == __main__:
    watchdog()
