import bottle
import dbutils
from models import finances, users
import pages

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

def percents(n:int, mx:int, digits:int=1) -> float:
    return round((n/mx)*100, digits)

class Finances(pages.Page):
    @yield_handler
    def get(self):
        if not pages.auth.current().userlevel.admin():
            raise bottle.HTTPError(404)
        with dbutils.dbopen() as db:
            month = int(bottle.request.query.get('month', 0))
            fin = finances.Finances(month, db)
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
    get.route = '/admin/finances'