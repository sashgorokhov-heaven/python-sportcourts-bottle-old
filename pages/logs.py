import bottle
import pages
import dbutils
from models import logs

def yield_handler(func):
    def wrapper(*args, **kwargs):
        if 'text' in bottle.request.query or True:
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

def percents(n:int, mx:int, digits:int=1) -> float:
    return round((n/mx)*100, digits)

class Logs(pages.Page):
    @yield_handler
    def get(self):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
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

    get.route = '/admin/logs'