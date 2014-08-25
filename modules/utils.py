import datetime
import smtplib

from modules import dbutils, config


_months = ['Января', 'Февраля',
           'Марта', 'Апреля',
           'Мая', 'Июня', 'Июля',
           'Августа', 'Сентября',
           'Октября', 'Ноября', 'Декабря']
_days = ['Понедельник', 'Вторник', 'Среда',
         'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def beautifuldate(datetime:str):
    date, day = datetime.split(' ')[0].split('-')[1:]
    return '{} {}'.format(day, _months[int(date) - 1])


def beautifultime(datetime:str):
    return ':'.join(datetime.split(' ')[-1].split(':')[:-1])


def beautifulday(datetime_:str):
    return _days[datetime.date(*list(map(int, datetime_.split(' ')[0].split('-')))).weekday()]


def get_notifications(user_id:int) -> list:
    with dbutils.dbopen() as db:
        db.execute("SELECT * FROM notifications WHERE user_id='{}' AND `read`=0 ORDER BY datetime DESC".format(user_id),
                   dbutils.dbfields['notifications'])
        notifications = db.last()
        if len(notifications) > 0:
            db.execute("UPDATE notifications SET `read`='1' WHERE notification_id IN ({})".format(
                ','.join([str(i['notification_id']) for i in notifications])))
        return notifications


def get_notifycount(user_id:int) -> int:
    if user_id == 0: return 0
    with dbutils.dbopen() as db:
        return len(db.execute(
            "SELECT * FROM notifications WHERE user_id={} AND `read`=0 ORDER BY DATETIME DESC".format(user_id)))


def write_notification(user_id:int, notification:str, level:int=0):
    with dbutils.dbopen() as db:
        db.execute(
            "INSERT INTO notifications (user_id, datetime, text, level) VALUES ({}, NOW(), '{}', {})".format(user_id,
                                                                                                             str(
                                                                                                                 notification),
                                                                                                             level))


def sendmail(message:str, to:str, subject:str='Уведомление'):
    try:
        me = config['email']['login']
        you = to
        text = str(message)
        subj = '{} | Sportcourts | Спортивные площадки'.format(subject)
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