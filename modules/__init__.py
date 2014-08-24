import json
import os
import random
import itertools
import smtplib
import traceback
import time

import bottle


config = json.load(open(os.path.join('modules', 'config.json'), 'r'))


def _generate_secret():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(10, 30)))


def extract_traceback(e):
    return '\n'.join(traceback.format_exception(e.__class__, e, e.__traceback__))


def generate_token():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(30, 40)))


config['secret'] = _generate_secret()


def sendmail(message:str, to:str):
    try:
        me = config['email']['login']
        you = to
        text = str(message)
        subj = 'Уведомление | Sportcourts | Спортивные площадки'
        server = "smtp.gmail.com"
        port = 25
        user_name = config['email']['login']
        user_passwd = config['email']['password']
        msg = smtplib.email.mime.text.MIMEText(text, _charset="utf-8")
        msg['Subject'] = subj
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP(server, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user_name, user_passwd)
        s.sendmail(me, you, msg.as_string())
        s.quit()
    except Exception as e:
        return False
    return True


def exec_time_measure(callback):
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs)
        end = time.time()
        bottle.response.headers['X-Exec-Time'] = str(end - start)
        return body

    return wrapper
