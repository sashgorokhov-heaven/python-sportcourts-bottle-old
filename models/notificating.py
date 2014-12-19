import json
import smtplib
from email.mime import text
from email.mime import multipart

import dbutils
import config
from models import autodb, users
import urllib.request, urllib.parse
import pages
import cacher
from modules import logging


def _send_message(email, message):
    smtp = smtplib.SMTP("smtp.gmail.com", 25)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(config.email.login, config.email.password)
    smtp.sendmail(config.email.login, email, message.as_string())
    smtp.quit()


class mail:
    @staticmethod
    def raw(subject:str, body:str, email:str):
        message = text.MIMEText(body, _charset="utf-8")
        message['Subject'] = '{} | Sportcourts | Спортивные площадки'.format(subject)
        message['From'] = config.email.login
        message['To'] = email
        return _send_message(email, message)

    @staticmethod
    @autodb
    def raw_to_id(subject:str, body:str, user_id:int, dbconnection:dbutils.DBConnection=None):
        user = users.get(user_id, dbconnection=dbconnection)
        email = user.email()
        return mail.raw(subject, body, email)

    @staticmethod
    def html(subject:str, body:str, email:str, plain:str=None):
        message = multipart.MIMEMultipart('alternative')
        message['Subject'] = '{} | Sportcourts | Спортивные площадки'.format(subject)
        message['From'] = config.email.login
        message['To'] = email
        if plain:
            message.attach(text.MIMEText(plain, 'plain'))
        message.attach(text.MIMEText(body, 'html'))
        return _send_message(email, message)

    @staticmethod
    @autodb
    def html_to_id(subject:str, body:str, user_id:int, plain:str=None, dbconnection:dbutils.DBConnection=None):
        user = users.get(user_id, dbconnection=dbconnection)
        email = user.email()
        if user.settings.send_mail():
            return mail.html(subject, body, email, plain)

    class tpl:
        @staticmethod
        def oncoming_game(game, user):
            html_email = pages.PageBuilder('mail_notify', game=game, user=user).template()
            email = user.email()
            plain = 'Уведомление о приближающейся игре - надо заполнить, но лень. Напишите vk.com/sashgorokhov, если прочли это.'
            subject = 'Уведомление о приближающейся игре'
            if user.settings.send_mail():
                mail.html(subject, html_email, email, plain)

        @staticmethod
        def email_confirm(token:str, email:str):
            html_email = pages.PageBuilder('mail_a1', token=token).template()
            plain = 'Чтобы подтвердить email, перейдите по ссылке http://{}/registration?token={}'.format(config.server, token)
            subject = 'Подверждение адреса электронной почты'
            mail.html(subject, html_email, email, plain)

        @staticmethod
        def email_confirm_again(token:str, email:str):
            html_email = pages.PageBuilder('mail_a2', token=token).template()
            plain = 'Чтобы подтвердить email, перейдите по ссылке http://{}/registration?token={}'.format(config.server, token)
            subject = 'Повторное подверждение адреса электронной почты'
            mail.html(subject, html_email, email, plain)

        @staticmethod
        def game_invite(game, user):
            html_email = pages.PageBuilder('mail_invite', game=game, user=user).template()
            email = user.email()
            plain = 'Приглашаем вас на игру http://{}/games/{}'.format(config.server.str, game.game_id())
            subject = 'Приглашение на игру'
            if user.settings.send_mail():
                try:
                    mail.html(subject, html_email, email, plain)
                except Exception as e:
                    logging.message("Error sending email to <{}>".format(email), e)


class site:
    @staticmethod
    @autodb
    def raw(user_id:int, text:str, level:int=0, game_id:int=0, type:int=0, date_time:str=None, dbconnection:dbutils.DBConnection=None):
        dbconnection.execute(
            "INSERT INTO notifications (user_id, text, level, game_id, type, datetime) VALUES ({}, '{}', {}, {}, {}, {})".format(
                user_id, text, level, game_id, type,
                'NOW()' if not date_time else "{}".format(date_time)))
        cacher.drop('notifications_count', user_id)

    @staticmethod
    @autodb
    def all(user_id:int, text:str, level:int=0, game_id:int=0, date_time:str=None, dbconnection:dbutils.DBConnection=None):
        return site.raw(user_id, text, level, game_id, 0, date_time, dbconnection=dbconnection)

    @staticmethod
    @autodb
    def subscribed(user_id:int, text:str, level:int=0, game_id:int=0, date_time:str=None, dbconnection:dbutils.DBConnection=None):
        return site.raw(user_id, text, level, game_id, 1, date_time, dbconnection=dbconnection)

    @staticmethod
    @autodb
    def responsible(user_id:int, text:str, level:int=0, game_id:int=0, date_time:str=None, dbconnection:dbutils.DBConnection=None):
        return site.raw(user_id, text, level, game_id, 2, date_time, dbconnection=dbconnection)


class SmsSendingError(Exception):
    def __init__(self, code:int, descr:str):
        self.code = code
        self.descr = descr
        super().__init__(descr)

    def __str__(self):
        return '{} <{}>: {}'.format(self.__class__.__name__, self.code, self.descr)


class sms:
    @staticmethod
    def raw(phone:str, text:str, source:str=None, idGroup:int=None, flash:int=0, onlydelivery:int=0):
        params = {'login': config.sms.login, 'password': config.sms.password, 'txt': text, 'to':phone}
        if source:
            params['source'] = source
        if flash:
            params['flash'] = flash
        if idGroup:
            params['idGroup'] = idGroup
        if onlydelivery:
            params['onlydelivery'] = onlydelivery
        f = urllib.request.urlopen('https://lcab.sms-uslugi.ru/lcabApi/sendSms.php?{}'.format(urllib.parse.urlencode(params)))
        body = json.loads(f.read().decode())
        if body['code']!=1:
            raise SmsSendingError(body['code'], body['descr'])
        return body['colsmsOfSending'], body['priceOfSending']

    @staticmethod
    @autodb
    def sms_to_id(user_id:int, text:str, source:str=None, dbconnection:dbutils.DBConnection=None):
        user = users.get(user_id, dbconnection=dbconnection)
        phone = user.phone()
        if not phone:
            raise ValueError('Invalid number <{}> - <{}>'.format(user_id, phone))
        return sms.raw(phone, text, source)