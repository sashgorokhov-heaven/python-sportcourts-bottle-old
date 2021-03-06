import bottle
import json
import os
import datetime
import cacher
import config
from modules import logging
import pages
import dbutils
from models import finances, logs, users, notificating, sport_types, courts
from modules.myuwsgi import uwsgi, uwsgidecorators
from objects import mydatetime


def get_users(db:dbutils.DBConnection) -> dict:
    users_ = db.execute("SELECT user_id, first_name, last_name, email, phone  FROM users",
                       ['user_id', 'first_name', 'last_name', 'email', 'phone'])
    return {'users': json.dumps(users_,ensure_ascii=False)}


def get_courts(db:dbutils.DBConnection) -> dict:
    courts_ = db.execute("SELECT court_id, title, cost, sport_types, phone  FROM courts",
                       ['court_id', 'title', 'cost', 'sport_types', 'phone'])
    return {'courts': json.dumps(courts_,ensure_ascii=False)}


def get_logs(db:dbutils.DBConnection) -> dict:
    return {'log':logs.Logs(db)}


@pages.get(['/admin', '/admin/'])
@pages.only_admins
def index():
    with dbutils.dbopen() as db:
        respdict = get_users(db)
        fin = finances.get_current_month(dbconnection=db)
        fin = finances.Finances(fin, db)
        respdict.update(get_logs(db))
        return pages.PageBuilder('admin', fin=fin, **respdict)


def percents(n:int, mx:int, digits:int=1) -> float:
    return round((n/mx)*100, digits)


def yield_handler(func):
    def wrapper(*args, **kwargs):
        if 'text' in bottle.request.query:
            resp = list()
            try:
                for line in func(*args, **kwargs):
                    resp.append(line)
            except Exception as e:
                resp.append(e.__class__.__name__)
                resp.append(e.args)
                return '<br>'.join(map(str, resp))
            return '<br>'.join(map(str, resp))
        else:
            return list(func(*args, **kwargs))[0]
    return wrapper


@pages.get('/admin/users')
@pages.only_admins
def index():
    with dbutils.dbopen() as db:
        respdict = get_users(db)
        return pages.PageBuilder('userbase', **respdict)


@pages.get('/admin/courts')
@pages.only_admins
def index():
    with dbutils.dbopen() as db:
        respdict = get_courts(db)
        return pages.PageBuilder('courtsbase', **respdict)


@pages.get('/admin/sms')
@pages.only_admins
def sms():
    return pages.PageBuilder('smstest')


@pages.get('/admin/email')
@pages.only_admins
def sms():
    return pages.PageBuilder('email')


@pages.get('/admin/social/groupadd')
@pages.only_admins
def groupadd():
    with dbutils.dbopen() as db:
        _sport_types = sport_types.get(0, dbconnection=db)
        return pages.PageBuilder('groupadd', sports=_sport_types)


@pages.get('/admin/social/spam')
@pages.only_admins
def spam():
    with dbutils.dbopen() as db:
        _sport_types = sport_types.get(0, dbconnection=db)
        return pages.PageBuilder('spam', sports=_sport_types)


#@pages.get('/admin/loadfinances')
#@pages.only_admins
#def load_finances():
#    with dbutils.dbopen() as db:
#        fin = finances.Finances(10, db=db)
#        db.execute("INSERT INTO finances VALUES (2014, 10, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
#            len(fin.games), fin.ideal_income, fin.empty, fin.lost_empty, fin.notvisited,
#            fin.lost_notvisited, fin.notpayed, fin.lost_notpayed, len(fin.played_users),
#            len(fin.played_unique), fin.real_income, fin.rent_charges, fin.profit
#        ))
#
#        fin = finances.Finances(11, db=db)
#
#        db.execute("INSERT INTO finances VALUES (2014, 11, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
#            len(fin.games), fin.ideal_income, fin.empty, fin.lost_empty, fin.notvisited,
#            fin.lost_notvisited, fin.notpayed, fin.lost_notpayed, len(fin.played_users),
#            len(fin.played_unique), fin.real_income, fin.rent_charges, fin.profit
#        ))

@pages.get('/admin/logs')
@pages.only_admins
def logs_page():
    with dbutils.dbopen(**dbutils.logsdb_connection) as db:
        page = pages.PageBuilder('logs', logs=logs.Logs(db), prob_den=finances.probability_density())
    with dbutils.dbopen() as db:
        dates = db.execute("SELECT regdate FROM users ORDER BY regdate ASC")
        page.add_param("start_date", dates[0][0])
        page.add_param("end_date", dates[-1][0])
        dates = list(map(lambda x: str(x[0]), dates))
        dates_dict = dict()
        for date in dates:
            if date in dates_dict:
                dates_dict[date] += 1
            else:
                dates_dict[date] = 1
        #page.add_param("dates", dates)
        page.add_param("dates_dict", dates_dict)

        def daterange(start_date, end_date):
            for n in range(int ((end_date - start_date).days)):
                yield start_date + datetime.timedelta(n)
        page.add_param("daterange", daterange)


    return page


@pages.get('/admin/logs/text')
@pages.only_admins
@yield_handler
def logs_page_text():
    with dbutils.dbopen(**dbutils.logsdb_connection) as db:
        logs_ = logs.Logs(db)
        yield 'Посещений в этом месяце: {} ({} уникальных {}%)'.format(len(logs_.logs), len(logs_.ips), percents(len(logs_.ips), len(logs_.logs)))
        this_week = sum([len(day) for day in logs_.this_week])
        unique_week = {logs_.logs_dict[i]['ip'] for day in logs_.this_week for i in day}
        yield 'Посещений в на этой неделе: {} ({}%) ({} уникальных {}%)'.format(this_week, percents(this_week, len(logs_.logs)), len(unique_week), percents(len(unique_week), this_week))
        unique_day = {logs_.logs_dict[i]['ip'] for i in logs_.today}
        yield 'Посещений сегодня: {} ({}%) ({} уникальных {}%)'.format(len(logs_.today), percents(len(logs_.today), this_week), len(unique_day), percents(len(unique_day), len(logs_.today)))
        yield ''
        registered = len(logs_.ips-set(list(logs_.users_by_ips)))
        yield 'Пользователей в системе: {} ({}%)'.format(registered, percents(registered, len(logs_.ips)))


@pages.get('/admin/reload')
@pages.only_admins
def reload():
    referer = bottle.request.get_header("Referer", "/")
    uwsgi.reload()
    raise bottle.redirect(referer)


@uwsgidecorators.filemon(os.path.join(config.paths.server.root, 'pages'))
def reload_on_pages_change(*args):
    uwsgi.reload()


@pages.post('/admin/poster')
def poster():
    resp = list()
    for i in bottle.request.forms:
        resp.append('<b>{}:&nbsp</b>{}'.format(i, bottle.request.forms.get(i)))
    return '<br>'.join(resp)


@pages.get('/showtpl/<tplname>')
@pages.only_admins
def show_template(tplname:str):
    return pages.PageBuilder(tplname, **{i:bottle.request.query.get(i) for i in bottle.request.query})


@pages.get('/admin/sendsms')
@pages.only_admins
def sendsms():
    return pages.PageBuilder('sendsms')


@pages.post('/admin/sendsms')
@pages.only_admins
def sendsms_post():
    phone = bottle.request.forms.get('phone')
    text = bottle.request.forms.get('text')
    notificating.sms.raw(phone, text)
    raise bottle.redirect('/admin/sendsms')


#@uwsgidecorators.cron(0,0, 1,-1, -1)
#def calc_finances(*args):
#    yesterday = datetime.date.today()-datetime.timedelta(days=1)
#    year = yesterday.year
#    month = yesterday.month
#    try:
#        with dbutils.dbopen() as db:
#            fin = finances.Finances(month, year, db=db)
#            db.execute("INSERT INTO finances VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
#                year, month,
#                len(fin.games), fin.ideal_income, fin.empty, fin.lost_empty, fin.notvisited,
#                fin.lost_notvisited, fin.notpayed, fin.lost_notpayed, len(fin.played_users),
#                len(fin.played_unique), fin.real_income, fin.rent_charges, fin.profit
#            ))
#    except Exception as e:
#        logging.message('Error calcing finances for <{}:{}>'.format(month, year), e)


@uwsgidecorators.cron(0,0, 1,-1, -1)
def drop_logs(*args):
    yesterday = datetime.date.today()-datetime.timedelta(days=1)
    year = yesterday.year
    month = yesterday.month
    sql = """CREATE TABLE logsdb.`{month}_{year}` (
             	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
             	`datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
             	`ip` VARCHAR(15) NOT NULL,
             	`time` FLOAT UNSIGNED NOT NULL DEFAULT '0',
             	`httpmethod` VARCHAR(10) NOT NULL DEFAULT 'GET',
             	`path` VARCHAR(200) NOT NULL,
             	`referer` VARCHAR(200) NOT NULL,
             	`user_id` INT UNSIGNED NOT NULL DEFAULT '0',
             	`useragent` VARCHAR(1000) NOT NULL,
             	`error` VARCHAR(5000) NULL DEFAULT NULL,
             	`error_description` VARCHAR(5000) NULL DEFAULT NULL,
             	`traceback` VARCHAR(10000) NULL DEFAULT NULL,
             	PRIMARY KEY (`id`),
             	UNIQUE INDEX `id` (`id`)
             )
             COLLATE='utf8_general_ci'
             ENGINE=MyISAM
             SELECT * FROM logsdb.access WHERE MONTH(datetime)={month} AND YEAR(datetime)={year};
    """.format(month=month, year=year)
    with dbutils.dbopen(**dbutils.logsdb_connection) as db:
        try:
            db.execute(sql)
        except:
            return
        else:
            db.execute("DELETE FROM logsdb.access WHERE MONTH(datetime)={} AND YEAR(datetime)={}".format(month, year))


@pages.get('/admin/drop_cache')
@pages.only_admins
def drop_cache():
    cacher.dropall()
    raise bottle.redirect('/admin')


@pages.get('/admin/conv')
@pages.only_admins
def conversion():
    return str(logs.conversion())


@pages.post('/admin/outlays/addnegative')
@pages.only_admins
def get_add_outlays():
    param = lambda x: bottle.request.forms.get(x)
    dt = param('date') + ' ' + param('time') + ':00'
    finances.add_outlay(dt, param('title'), param('description'), -int(param('cost')))
    raise bottle.redirect("/admin/finances")

@pages.post('/admin/outlays/add')
@pages.only_admins
def get_add_outlays():
    param = lambda x: bottle.request.forms.get(x)
    dt = param('date') + ' ' + param('time') + ':00'
    finances.add_outlay(dt, param('title'), param('description'), param('cost'))
    raise bottle.redirect("/admin/finances")


@pages.get('/admin/add_game_finance/<game_id:int>')
@pages.only_admins
def add_game_finance(game_id:int):
    finances.add_game_finances(game_id)


@pages.get('/admin/recalc_game/<game_id:int>')
@pages.only_admins
def recalc_game(game_id:int):
    finances.update_game_finances(game_id)


@pages.get(['/admin/finances', '/admin/finances/<month:int>', '/admin/finances/<month:int>/<year:int>'])
@pages.only_admins
def new_finances(month:int=0, year:int=0):
    with dbutils.dbopen() as db:
        dates = db.execute("SELECT DISTINCT MONTH(datetime), YEAR(datetime) FROM finances ORDER BY datetime DESC")
        if not month:
            month = datetime.date.today().month
        if not year:
            month = datetime.date.today().month
            year = datetime.date.today().year
        outlays = finances.get_outlays_by_date(month, year, dbconnection=db)
        games_finances = finances.get_by_date(month, year, dbconnection=db)
        fin = finances.Finances(games_finances, db)
        dates = list(map(lambda x: ('{}/{}'.format(*x), '{} {}'.format(mydatetime._months[x[0]-1], x[1])), dates))
        return pages.PageBuilder('finances', dates=dates, current_date='{}/{}'.format(month, year),
                                 fin=fin, outlays=outlays)


@pages.get('/admin/finances/recount')
@pages.only_admins
def recount_finances():
    with dbutils.dbopen() as db:
        db.execute("TRUNCATE finances;")
        db.execute("TRUNCATE responsible_games_salary;")
        db.execute("DELETE FROM finance_balance WHERE user_id!=0")
        db.execute("SELECT game_id FROM games WHERE deleted=0 AND datetime<NOW() AND game_id IN (SELECT DISTINCT game_id FROM reports)")
        for game_id in db.last().copy():
            finances.add_game_finances(game_id[0], dbconnection=db)
        raise bottle.redirect('/admin/finances')