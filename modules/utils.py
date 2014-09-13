import datetime
import threading

from modules import dbutils


_months = ['Января', 'ФевралЯ',
           'Марта', 'Апреля',
           'Мая', 'Июня', 'Июля',
           'Августа', 'Сентября',
           'Октября', 'Ноября', 'Декабря']

_months_game = ['Январь', 'Февраль',
           'Март', 'Апрель',
           'Май', 'Июнь', 'Июль',
           'Август', 'Сентябрь',
           'Октябрь', 'Ноябрь', 'Декабрь']

_days = ['Понедельник', 'Вторник', 'Среда',
         'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def beautifuldate(datetime:str, gamespage:bool=False):
    date, day = datetime.split(' ')[0].split('-')[1:]
    return (day, _months_game[int(date) - 1]) if gamespage else '{} {}'.format(day, _months[int(date) - 1])


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


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=func.__qualname__)
        thread.start()
        return thread

    return wrapper