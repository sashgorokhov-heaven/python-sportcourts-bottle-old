import dbutils
from models import sport_types, autodb, users
from objects import Game, Court, Outlay, GameFinance

def group(key, iterable) -> dict:
    d = dict()
    for i in iterable:
        if key(i) not in d:
            d[key(i)] = [i]
        else:
            d[key(i)].append(i)
    return d

def probability_density():
    with dbutils.dbopen() as db:
        reports = db.execute("SELECT * FROM reports WHERE user_id!=0", dbutils.dbfields['reports'])
        notplayed = db.execute("SELECT COUNT(*) FROM users WHERE user_id NOT IN (SELECT DISTINCT user_id FROM reports)")[0][0]
        visits = dict()
        for i in reports:
            user_id = i['user_id']
            if user_id not in visits:
                visits[user_id] = 1
            else:
                visits[user_id] += 1
        density = dict()
        visits_val = set(list(visits.values()))
        for n in visits_val:
            density[n] = len(list(filter(lambda x: n==visits[x], visits)))
        return {'visits':visits, 'density':density, 'notplayed':notplayed, 'visits_val':visits_val}


@autodb
def get_all_outlays(dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM outlays", dbutils.dbfields['outlays'])
    return list(map(Outlay, dbconnection.last()))


@autodb
def get_outlays_by_date(month:int=0, year:int=0, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM outlays WHERE MONTH(datetime)={} AND YEAR(datetime)={}".format(
        'NOW()' if month==0 else month,
        'NOW()' if year==0 else year), dbutils.dbfields['outlays'])
    return list(map(Outlay, dbconnection.last()))


@autodb
def get_current_month_outlays(dbconnection:dbutils.DBConnection=None):
    return get_outlays_by_date(dbconnection=dbconnection)


def add_outlay(datetime:str, title:str, description:str, cost:int):
    with dbutils.dbopen() as db:
        db.execute("INSERT INTO outlays (datetime, title, description, cost) VALUES ('{}', '{}', '{}', {})".format(
            datetime, title, description, cost))


class Finances:
    @staticmethod
    def percents(n:int, mx:int, digits:int=1) -> int:
        return round((n/mx)*100, digits) if mx!=0 else 0

    def __init__(self, game_finances_list:list, db:dbutils.DBConnection):
        self.games = game_finances_list
        self.games_dict = {game.game_id():game for game in self.games}
        self.sports = {sport.sport_id():sport for sport in sport_types.get(0, dbconnection=db)}
        self.real_games = db.execute("SELECT * FROM games WHERE game_id IN ({})".format(
            ', '.join(list(map(str, self.games_dict.keys())))), dbutils.dbfields['games']) if len(self.games)>0 else list()
        self.real_games_dict = {game['game_id']:game for game in self.real_games}
        summ = lambda field: sum([getattr(game, field)() for game in self.games])

        self.ideal_income = summ('ideal_income')
        self.empty = summ('empty')
        self.lost_empty = summ('lost_empty')
        self.notvisited = summ('notvisited')
        self.lost_notvisited = summ('lost_notvisited')
        self.notpayed = summ('notpayed')
        self.lost_notpayed = summ('lost_notpayed')
        self.real_income = summ('real_income')
        self.rent_charges = summ('rent_charges')
        self.additional_charges = summ('additional_charges')
        self.profit = summ('profit')
        self.responsible_salary = summ('responsible_salary')
        self.real_profit = summ('real_profit')

        self.game_by_responsible = group(lambda x: x.responsible_user_id(), self.games)

        a = db.execute("SELECT * FROM responsible_games_salary WHERE game_id IN ({})".format(
            ', '.join([str(game.game_id()) for game in self.games])), dbutils.dbfields['responsible_games_salary']) if len(self.games)>0 else list()
        self.salary = group(lambda x: x['user_id'], a)
        self.users_get = users.get

        self.sport_games = group(lambda x: x.sport_id(), self.games)

        self.sport_money = dict()
        for sport_id in self.sport_games:
            self.sport_money[sport_id] = sum([game.real_profit() for game in self.sport_games[sport_id]])

        a = db.execute("SELECT * FROM finance_balance WHERE user_id!=0 AND YEAR(date)={} AND MONTH(date)={}".format(
            self.games[-1].datetime().date().year, self.games[0].datetime().date().month
        ), dbutils.dbfields['finance_balance']) if len(self.games)>0 else list()
        self.user_salary = {i['user_id']:i['value'] for i in a}


@autodb
def calc_game(game_id:int, dbconnection:dbutils.DBConnection=None) -> dict:
    game = dbconnection.execute("SELECT * FROM games WHERE game_id={}".format(game_id), dbutils.dbfields['games'])[0]
    game = Game(game, dbconnection=dbconnection)
    reports = dbconnection.execute("SELECT * FROM reports WHERE game_id={}".format(game_id), dbutils.dbfields['reports'])
    additional_charges = dbconnection.execute("SELECT * FROM additional_charges WHERE game_id={}".format(game_id), dbutils.dbfields['additional_charges'])

    finances = dict()
    finances['game_id'] = game_id
    finances['datetime'] = game.datetime()
    finances['capacity'] = game.capacity()
    finances['cost'] = game.cost()
    finances['sport_id'] = game.sport_type()
    finances['responsible_user_id'] = game.responsible_user_id()
    finances['created_by'] = game.created_by()

    finances['visited'] = len(list(filter(lambda x: x['status']!=0, reports)))
    finances['empty'] = finances['capacity']-finances['visited']
    if finances['empty']<0: finances['empty']=0
    finances['lost_empty'] = finances['empty']*finances['cost']
    finances['notvisited'] = len(list(filter(lambda x: x['status']==0, reports)))
    finances['lost_notvisited'] = finances['notvisited']*finances['cost']
    finances['notpayed'] = len(list(filter(lambda x: x['status']==1, reports)))
    finances['lost_notpayed'] = finances['notpayed']*finances['cost']

    finances['playedpayed'] = len(list(filter(lambda x: x['status']==2, reports)))
    finances['real_income'] = finances['playedpayed']*finances['cost']
    finances['ideal_income'] = finances['cost']*finances['capacity'] if finances['capacity']>0 else finances['real_income']
    finances['rent_charges'] = game.court_id(True).cost()*(game.duration()/60)
    finances['additional_charges'] = sum([i['cost'] for i in additional_charges])

    finances['profit'] = finances['real_income']-finances['additional_charges']-finances['rent_charges']

    dbconnection.execute("SELECT percents FROM responsible_salary WHERE user_id={}".format(game.responsible_user_id()))
    finances['responsible_salary'] = 0
    if len(dbconnection.last())>0:
        finances['responsible_salary'] = round((finances['profit'])*(dbconnection.last()[0][0]/100))
    finances['profit'] -= finances['responsible_salary']

    finances['real_profit'] = finances['profit'] + finances['rent_charges']

    return finances

@autodb
def add_game_finances(game_id:int, dbconnection:dbutils.DBConnection=None):
    finances = calc_game(game_id, dbconnection=dbconnection)
    sql = "INSERT INTO finances VALUES ({})".format(', '.join(["'{}'".format(finances[i]) for i in dbutils.dbfields['finances']]))
    dbconnection.execute(sql)
    dbconnection.execute("SELECT percents FROM responsible_salary WHERE user_id={}".format(finances['responsible_user_id']))
    if len(dbconnection.last())>0:
        percents = dbconnection.last()[0][0]
        dbconnection.execute("INSERT INTO responsible_games_salary VALUES ({}, {}, {}, {}, {})".format(
            finances['responsible_user_id'], game_id, finances['profit'], percents, finances['responsible_salary']))
    dbconnection.execute("SELECT * FROM finance_balance WHERE user_id!=0 AND YEAR(date)={} AND MONTH(date)={}".format(
        finances['datetime'].date().year, finances['datetime'].date().month), dbutils.dbfields['finance_balance'])
    if len(dbconnection.last())==0:
        dbconnection.execute("INSERT INTO finance_balance VALUES ('Александр Горохов', 0, 3, '{year}-{month}-01', 50), ('Виталий Харченко', 0, 1, '{year}-{month}-01', 50)".format(
            year=finances['datetime'].date().year, month=finances['datetime'].date().month))
    owners = dbconnection.last()
    balance = dbconnection.execute("SELECT * FROM finance_balance WHERE user_id=0", dbutils.dbfields['finance_balance'])[0]
    for owner in owners:
        percents = owner['percents']
        money = round(finances['real_profit']*(percents/100))
        if owner['user_id']==finances['responsible_user_id']:
            money += finances['responsible_salary']
        dbconnection.execute("UPDATE finance_balance SET value=value+{} WHERE user_id={} AND YEAR(date)={} AND MONTH(date)={}".format(
            money, owner['user_id'], finances['datetime'].date().year, finances['datetime'].date().month))
    percents = balance['percents']
    money = finances['real_profit']*(percents/100)
    dbconnection.execute("UPDATE finance_balance SET value=value+{} WHERE user_id=0".format(money))


@autodb
def update_game_finances(game_id:int, dbconnection:dbutils.DBConnection=None):
    finances = calc_game(game_id, dbconnection=dbconnection)
    sql = "UPDATE finances SET {} WHERE game_id={}".format(', '.join(["{}='{}'".format(i, finances[i]) for i in dbutils.dbfields['finances'] if i!='game_id']), game_id)
    dbconnection.execute(sql)


@autodb
def get(game_id:int, dbconnection:dbutils.DBConnection=None) -> GameFinance:
    dbconnection.execute("SELECT * FROM finances WHERE game_id={}".format(game_id), dbutils.dbfields['finances'])
    if len(dbconnection.last())==0:
        return None
    return GameFinance(dbconnection.last()[0])


@autodb
def get_all(dbconnection:dbutils.DBConnection=None) -> GameFinance:
    dbconnection.execute("SELECT * FROM finances", dbutils.dbfields['finances'])
    return list(map(lambda x: GameFinance(x, dbconnection), dbconnection.last()))


@autodb
def get_by_date(month:int=0, year:int=0, dbconnection:dbutils.DBConnection=None) -> GameFinance:
    dbconnection.execute("SELECT * FROM finances WHERE MONTH(datetime)={} AND YEAR(datetime)={}".format(
        'MONTH(NOW())' if month==0 else month,
        'YEAR(NOW())' if year==0 else year), dbutils.dbfields['finances'])
    return list(map(lambda x: GameFinance(x, dbconnection), dbconnection.last()))

@autodb
def get_current_month(dbconnection:dbutils.DBConnection=None) -> GameFinance:
    return get_by_date(dbconnection=dbconnection)

@autodb
def get_additional_charges(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM additional_charges WHERE game_id={}".format(game_id), dbutils.dbfields['additional_charges'])
    return dbconnection.last()