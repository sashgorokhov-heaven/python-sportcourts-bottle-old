from .myuwsgi import uwsgidecorators
import dbutils
import datetime
from objects import Game
from models import mailing
from . import logging


_tasks = list()


def add_task(func):
    _tasks.append(func)
    return func


@uwsgidecorators.timer(720, target='spooler') # 720s = 12min
def main_timer(*args):
    for func in _tasks:
        try:
            func()
        except Exception as e:
            logging.message('Error on executing function <{}>'.format(func.__name__), e)


def send_notification(game:Game):
    if len(game.subscribed())==0:
        return
    for user in game.subscribed(True):
        try:
            mailing.emailtpl.oncoming_game(game, user)
        except Exception as e:
            logging.message('Error on sending email of upcoming game <{}> notification for <{}>'.format(game.game_id(), user.user_id()), e)


@add_task
def game_notification():
    with dbutils.dbopen() as db:
        db.execute("SELECT * FROM games WHERE deleted=0 AND notificated=0 AND NOW()<datetime", dbutils.dbfields['games'])
        if len(db.last())==0: return

        games = list(map(lambda x: Game(x, dbconnection=db), db.last()))

        weekdays = list(filter(lambda x: x.datetime.date().weekday()<5, games))
        weekends = list(filter(lambda x: x.datetime.date().weekday()>4, games))

        notify = list()

        if len(weekdays)>0:
            morning_day = list(filter(lambda x: x.datetime.time().hour<18, weekdays))
            if len(morning_day)>0:
                now = datetime.datetime.now()
                for game in morning_day:
                    if game.datetime.tommorow and 18<now.hour<19:
                        notify.append(game)
            evening = list(filter(lambda x: 18<=x.datetime.time().hour, weekdays))
            if len(evening)>0:
                now = datetime.datetime.now()
                for game in evening:
                    if game.datetime.today and 9<now.hour<10:
                        notify.append(game)
        if len(weekends)>0:
            morning_day = list(filter(lambda x: x.datetime.time().hour<18, weekends))
            if len(morning_day)>0:
                now = datetime.datetime.now()
                for game in morning_day:
                    if game.datetime.tommorow and 9<now.hour<10:
                        notify.append(game)
            evening = list(filter(lambda x: 18<=x.datetime.time().hour, weekends))
            if len(evening)>0:
                now = datetime.datetime.now()
                for game in evening:
                    if game.datetime.tommorow and 18<now.hour<19:
                        notify.append(game)

        for game in notify:
            try:
                send_notification(game)
            except Exception as e:
                logging.message('Error on sending upcoming game notifications for <{}>'.format(game.game_id()), e)
            else:
                db.execute("UPDATE games SET notificated=1 WHERE game_id={}".format(game.game_id()))


@add_task
def continue_registration():
    with dbutils.dbopen() as db:
        db.execute("SELECT token, email FROM activation WHERE activated=0 AND again=0 AND datetime+INTERVAL 6 HOUR BETWEEN NOW()-INTERVAL 12 MINUTE AND NOW()+INTERVAL 12 MINUTE")
        if len(db.last())==0: return
        for pair in db.last():
            mailing.emailtpl.email_confirm_again(*pair)
            db.execute("UPDATE activation SET again=1 WHERE email={}".format(pair[1]))