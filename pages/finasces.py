import bottle
import pages
import dbutils
from models import sport_types, users


def yield_handler(func):
    def wrapper(*args, **kwargs):
        try:
            resp = list()
            try:
                for line in func(*args, **kwargs):
                    resp.append(line)
            except Exception as e:
                resp.append(e.__class__.__name__)
                resp.append(e.args)
                return '<br>'.join(map(str, resp))
            return '<br>'.join(map(str, resp))
        except:
            raise
    return wrapper

def percents(n:int, max:int, digits:int=1) -> float:
    return round((n/max)*100, digits)

class Finances(pages.Page):

    @yield_handler
    def get(self, **kwargs):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            if 'month' in bottle.request.query:
                month = int(bottle.request.query.get('month'))
            else:
                month = 'MONTH(NOW())'
            games = db.execute("SELECT * FROM games WHERE "
                               "MONTH(datetime)={} AND "
                               "datetime+INTERVAL duration MINUTE<NOW() AND "
                               "game_id IN (SELECT game_id FROM reports)".format(month), dbutils.dbfields['games'])
            games_dict = {game['game_id']:game for game in games}

            if len(games_dict)==0:
                yield 'Игор нет. (небыло еще) (точнее не было отчетов)'
                raise StopIteration

            courts = db.execute("SELECT * FROM courts", dbutils.dbfields['courts'])
            courts_dict = {court['court_id']:court for court in courts}

            reports = db.execute("SELECT * FROM reports WHERE game_id IN ({})".format(', '.join(map(str, games_dict))),
                                 dbutils.dbfields['reports'])
            reports_dict = dict()
            for report in reports:
                if report['game_id'] not in reports_dict:
                    reports_dict[report['game_id']] = [report]
                else:
                    reports_dict[report['game_id']].append(report)

            delete_keys = list()
            for game_id in games_dict:
                if game_id not in reports_dict:
                    delete_keys.append(game_id)
            for game_id in delete_keys:
                games_dict.pop(game_id)
                p = None
                for n, game in enumerate(games):
                    if game['game_id']==game_id:
                        p = n
                        break
                games.pop(p)

            ideal_income = sum([game['capacity']*game['cost'] for game in games if game['capacity']>0])
            ideal_income += sum([len(reports_dict[game['game_id']])*game['cost'] for game in games if game['capacity']<0])

            yield 'Идеальный доход: {} ({} игр)'.format(ideal_income, len(games))

            played_users = list(filter(lambda x: x['status']==2,reports))
            played_unique = {i['user_id'] for i in played_users if i['user_id']!=0}
            yield 'Отыграло: {} ({} уникумов - {}%)'.format(len(played_users), len(played_unique), percents(len(played_unique), len(played_users)))

            # TODO везде где capacity проверять на capacity>0
            empty = sum([game['capacity']-len(list(filter(lambda x: x['status']>=0 and x['user_id']!=0, reports_dict[game['game_id']]))) for game in games])
            lost_empty = sum([(game['capacity']-len(list(filter(lambda x: x['status']>=0 and x['user_id']!=0, reports_dict[game['game_id']]))))*game['cost'] for game in games])
            yield 'Потеряно изза пустых мест: {} ({}%) ({})'.format(lost_empty, percents(lost_empty, ideal_income), empty)
            #ideal_income -= lost_empty

            notvisited = sum([len(list(filter(lambda x: x['status']==0, reports_dict[game['game_id']]))) for game in games])
            lost_notvisited = sum([len(list(filter(lambda x: x['status']==0, reports_dict[game['game_id']])))*game['cost'] for game in games])
            yield 'Потеряно изза непришедших: {} ({}%) ({})'.format(lost_notvisited, percents(lost_notvisited, ideal_income), notvisited)
            #ideal_income -= lost_notvisited

            notpayed = sum([len(list(filter(lambda x: x['status']==1, reports_dict[game['game_id']]))) for game in games])
            lost_notpayed = sum([len(list(filter(lambda x: x['status']==1, reports_dict[game['game_id']])))*game['cost'] for game in games])
            yield 'Потеряно изза неоплативших: {} ({}%) ({})'.format(lost_notpayed, percents(lost_notpayed, ideal_income), notpayed)
            #ideal_income -= lost_notpayed

            real_income = ideal_income-lost_empty-lost_notvisited-lost_notpayed

            yield 'Реальный доход: {} ({}%)'.format(real_income, percents(real_income, ideal_income))

            rent_charges = sum([courts_dict[game['court_id']]['cost']*(game['duration']/60) for game in games])
            yield 'Расходы на аренду: {} ({}%)'.format(rent_charges, percents(rent_charges, real_income))

            profit = real_income-rent_charges

            yield ''
            yield 'Прибыль: {} ({}%)'.format(profit, percents(profit, real_income))
            yield ''
            yield 'По видам спорта:'

            games_profit = {game['game_id']:len(list(filter(lambda x: x['status']==2, reports_dict[game['game_id']])))*game['cost']-courts_dict[game['court_id']]['cost']*(game['duration']/60) for game in games}
            #games_profit = {game['game_id']:len(list(filter(lambda x: x['status']==2, reports_dict[game['game_id']])))*game['cost'] for game in games}
            sport_games = dict()
            for game in games:
                if game['sport_type'] not in sport_games:
                    sport_games[game['sport_type']] = [game]
                else:
                    sport_games[game['sport_type']].append(game)
            sports = {sport.sport_id():sport for sport in sport_types.get(0, dbconnection=db)}

            sport_money = dict()
            for sport_id in sport_games:
                sport_money[sport_id] = sum([games_profit[game['game_id']] for game in sport_games[sport_id]])
                yield '{} ({} игр): {} ({}%)'.format(sports[sport_id].title(),
                                                     len(sport_games[sport_id]), sport_money[sport_id],
                                                     percents(sport_money[sport_id], profit))

            yield ''
            yield 'Зарплаты:'

            finances = db.execute("SELECT * FROM finances", dbutils.dbfields['finances'])
            finances_by_user = dict()
            for fin in finances:
                if fin['user_id'] not in finances_by_user:
                    finances_by_user[fin['user_id']] = [fin]
                else:
                    finances_by_user[fin['user_id']].append(fin)

            for user_id in finances_by_user:
                user = users.get(user_id, dbconnection=db)
                money = sum([sport_money[fin['sport_id']]*(fin['percents']/100) for fin in finances_by_user[user_id] if fin['sport_id'] in sport_money])
                yield '{}: {}р ({}%)'.format(user.name, money, percents(money, profit))

            yield ''
            yield 'Обсчитываемые игры:'
            for sport_id in sport_games:
                yield '{}:'.format(sports[sport_id].title())
                for game in sport_games[sport_id]:
                    yield '[{}] {} {} мест {}р {}мин'.format(game['game_id'], game['description'],
                                                             game['capacity'], game['cost'], game['duration'])
                    visited = len(list(filter(lambda x: x['status']==2, reports_dict[game['game_id']])))
                    rent = courts_dict[game['court_id']]['cost']*(game['duration']/60)
                    income = visited*game['cost']
                    profit = income-rent
                    yield 'Пришло {} чел и заплатило {}р   - {}р за аренду = {}'.format(visited, income, rent, profit)

            # TODO Самые популярные площадки

    get.route = '/fin'