import smtplib
from email.mime import text
from email.mime import multipart

from models import autodb, settings, users
from modules import config, dbutils, utils
import uwsgi

@utils.as_spooler
@utils.spooler('mailing_sendhtml')
def sendhtml(html:str, to:str, plain:str='Простой текст', subject:str='Уведомление'):
    try:
        me = config['email']['login']
        you = to

        server = "smtp.gmail.com"
        port = 25
        user_name = config['email']['login']
        user_passwd = config['email']['password']

        msg = multipart.MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you

        part1 = text.MIMEText(plain, 'plain')
        part2 = text.MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP(server, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user_name, user_passwd)
        s.sendmail(me, you, msg.as_string())
        s.quit()
    except Exception as e:
        #logging.error(e)
        return uwsgi.SPOOL_RETRY
    return uwsgi.SPOOL_OK


@utils.as_spooler
@utils.spooler('mailing_sendmail')
def sendmail(message:str, to:str, subject:str='Уведомление'):
    try:
        me = config['email']['login']
        you = to
        message = str(message)
        subj = '{} | Sportcourts | Спортивные площадки'.format(subject)
        server = "smtp.gmail.com"
        port = 25
        user_name = config['email']['login']
        user_passwd = config['email']['password']
        msg = text.MIMEText(message, _charset="utf-8")
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
        #logging.error(e)
        return uwsgi.SPOOL_RETRY
    return uwsgi.SPOOL_OK


@autodb
def send_to_user(user_id:int, message:str, subject:str='Уведомление', override:bool=False,
                 dbconnection:dbutils.DBConnection=None) -> bool:
    sett = settings.get(user_id, dbconnection=dbconnection)
    if not override and not sett.send_email():
        return True
    email = users.get(user_id, fields=['email'], dbconnection=dbconnection)['email']
    sendmail(message, email, subject)
