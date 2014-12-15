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

def get_finances(db:dbutils.DBConnection) -> dict:
    return {'fin':finances.Finances(0, 0, db=db)}


def get_users(db:dbutils.DBConnection) -> dict:
    users_ = db.execute("SELECT user_id, first_name, last_name, email, phone  FROM users",
                       ['user_id', 'first_name', 'last_name', 'email', 'phone'])
    return {'users': json.dumps(users_,ensure_ascii=False)}


def get_logs(db:dbutils.DBConnection) -> dict:
    return {'log':logs.Logs(db)}


@pages.get(['/admin', '/admin/'])
@pages.only_admins
def index():
    with dbutils.dbopen() as db:
        respdict = get_users(db)
        respdict.update(get_finances(db))
        respdict.update(get_logs(db))
        return pages.PageBuilder('admin', **respdict)


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

@pages.get('/admin/sms')
@pages.only_admins
def sms():
    return pages.PageBuilder('smstest')


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


@pages.get(['/admin/finances', '/admin/finances/<month:int>', '/admin/finances/<month:int>/<year:int>'])
@pages.only_admins
@yield_handler
def finances_page(month:int=0, year:int=0):
    with dbutils.dbopen() as db:
        fin = finances.Finances(month, year, db=db)

        if 'text' not in bottle.request.query:
            yield pages.PageBuilder('finances', **fin.dict()).template()
            raise StopIteration

        if len(fin.games)==0:
            yield 'Игор нет. (небыло еще) (точнее не было отчетов)'
            raise StopIteration

        yield 'Идеальный доход: {} ({} игр)'.format(fin.ideal_income, len(fin.games))
        yield 'Отыграло: {} ({} уникумов - {}%)'.format(len(fin.played_users),len(fin.played_unique),percents(len(fin.played_unique), len(fin.played_users)))
        yield 'Потеряно изза пустых мест: {} ({}%) ({})'.format(fin.lost_empty,percents(fin.lost_empty, fin.ideal_income),fin.empty)
        yield 'Потеряно изза непришедших: {} ({}%) ({})'.format(fin.lost_notvisited, percents(fin.lost_notvisited, fin.ideal_income),fin.notvisited)
        yield 'Потеряно изза неоплативших: {} ({}%) ({})'.format(fin.lost_notpayed,percents(fin.lost_notpayed, fin.ideal_income),fin.notpayed)
        yield 'Реальный доход: {} ({}%)'.format(fin.real_income, percents(fin.real_income, fin.ideal_income))
        yield 'Расходы на аренду: {} ({}%)'.format(fin.rent_charges, percents(fin.rent_charges, fin.real_income))
        yield ''
        yield 'Прибыль: {} ({}%)'.format(fin.profit, percents(fin.profit, fin.real_income))
        yield ''
        yield 'По видам спорта:'
        for sport_id in fin.sport_money:
            yield '{} ({} игр): {} ({}%)'.format(fin.sports[sport_id].title(), len(fin.sport_games[sport_id]), fin.sport_money[sport_id], percents(fin.sport_money[sport_id], fin.profit))
        yield ''
        yield 'Зарплаты:'
        for user_id in fin.user_salary:
            user = users.get(user_id, dbconnection=db)
            yield '{}: {}р ({}%)'.format(user.name, fin.user_salary[user_id], percents(fin.user_salary[user_id], fin.profit))
        yield ''
        yield 'Обсчитываемые игры:'
        for sport_id in fin.sport_games:
            yield '{}:'.format(fin.sports[sport_id].title())
            for game_id in fin.sport_games[sport_id]:
                game = fin.games_dict[game_id]
                yield '[{}] {} {} мест {}р {}мин'.format(game.game_id(), game.description(), game.capacity(), game.cost(), game.duration())
                yield 'Пришло {} чел и заплатило {}р   - {}р за аренду = {}'.format(fin.games_counted[game_id]['playedpayed'],
                                                                                    fin.games_counted[game_id]['real_income'],
                                                                                    fin.games_counted[game_id]['rent_charges'],
                                                                                    fin.games_counted[game_id]['profit'])


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


@uwsgidecorators.cron(0,0, 1,-1, -1)
def calc_finances(*args):
    yesterday = datetime.date.today()-datetime.timedelta(days=1)
    year = yesterday.year
    month = yesterday.month
    try:
        with dbutils.dbopen() as db:
            fin = finances.Finances(month, year, db=db)
            db.execute("INSERT INTO finances VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
                year, month,
                len(fin.games), fin.ideal_income, fin.empty, fin.lost_empty, fin.notvisited,
                fin.lost_notvisited, fin.notpayed, fin.lost_notpayed, len(fin.played_users),
                len(fin.played_unique), fin.real_income, fin.rent_charges, fin.profit
            ))
    except Exception as e:
        logging.message('Error calcing finances for <{}:{}>'.format(month, year), e)


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