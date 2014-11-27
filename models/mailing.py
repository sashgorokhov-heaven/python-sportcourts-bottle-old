import smtplib
from email.mime import text
from email.mime import multipart

import dbutils
from models import autodb, users
from modules import utils, logging
import config
from modules.myuwsgi import uwsgi
import pages

@utils.spool('mailing_sendhtml')
def sendhtml(html:str, to:str, plain:str='Простой текст', subject:str='Уведомление'):
    try:
        me = config.email.login
        you = to

        server = "smtp.gmail.com"
        port = 25
        user_name = config.email.login
        user_passwd = config.email.password

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
        logging.error(e)
        return uwsgi.SPOOL_RETRY
    return uwsgi.SPOOL_OK


@utils.spool('mailing_sendmail')
def sendmail(message:str, to:str, subject:str='Уведомление'):
    try:
        me = config.email.login
        you = to
        message = str(message)
        subj = '{} | Sportcourts | Спортивные площадки'.format(subject)
        server = "smtp.gmail.com"
        port = 25
        user_name = config.email.login
        user_passwd = config.email.password
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
        logging.error(e)
        return uwsgi.SPOOL_RETRY
    return uwsgi.SPOOL_OK


@autodb
def send_to_user(user_id:int, message:str, subject:str='Уведомление', override:bool=False,
                 dbconnection:dbutils.DBConnection=None):
    sett = users.get(user_id, dbconnection=dbconnection).settings
    if not override and not sett.send_email():
        return
    email = users.get(user_id, dbconnection=dbconnection).email()
    sendmail(message, email, subject)



class emailtpl:
    @staticmethod
    def oncoming_game(game, user):
        html_email = pages.PageBuilder('mail_notify', game=game, user=user).template()
        email = user.email()
        plain = 'Уведомление о приближающейся игре - надо заполнить, но лень. Напишите vk.com/sashgorokhov, если прочли это.'
        subject = 'Уведомление о приближающейся игре'
        sendhtml(html_email, email, plain, subject)