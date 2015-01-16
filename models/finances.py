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

    def __init__(self, month:int, year:int, db:dbutils.DBConnection):
        self._db = db

        if month==0:
            month = 'MONTH(NOW())'
            year = 'YEAR(NOW())'
        elif year==0:
            year = 'YEAR(NOW())'

        self.games = db.execute("SELECT * FROM games WHERE "
                                "MONTH(datetime)={} AND "
                                "YEAR(datetime)={} AND "
                                "datetime+INTERVAL duration MINUTE<NOW() AND "
                                "capacity>0 AND deleted=0 AND "
                                "game_id IN (SELECT game_id FROM reports) ORDER BY datetime DESC".format(month, year), dbutils.dbfields['games'])
        self.games = list(map(lambda x: Game(x, dbconnection=db), self.games))
        self.games_dict = {game.game_id():game for game in self.games}

        self.reports = db.execute("SELECT * FROM reports WHERE game_id IN ({})".format(', '.join(map(str, self.games_dict))),
                     dbutils.dbfields['reports']) if len(self.games)>0 else list()
        self.reports_dict = dict()

        self.additional_charges = db.execute("SELECT * FROM additional_charges WHERE game_id IN ({})".format(', '.join(map(str, self.games_dict))),
                                             dbutils.dbfields['additional_charges'])  if len(self.games)>0 else list()
        self.additional_charges_dict = dict()
        for charge in self.additional_charges:
            if charge['game_id'] in self.additional_charges_dict:
                self.additional_charges_dict[charge['game_id']].append(charge)
            else:
                self.additional_charges_dict[charge['game_id']] = [charge]

        for report in self.reports:
            if report['game_id'] not in self.reports_dict:
                self.reports_dict[report['game_id']] = [report]
            else:
                self.reports_dict[report['game_id']].append(report)

        self.courts = db.execute("SELECT * FROM courts", dbutils.dbfields['courts'])
        self.courts = list(map(lambda x: Court(x, dbconnection=db), self.courts))
        self.courts_dict = {court.court_id():court for court in self.courts}
        self.sports = {sport.sport_id():sport for sport in sport_types.get(0, dbconnection=db)}

        self.games_by_courts = {court_id:list(filter(lambda x: x.court_id()==court_id, self.games)) for court_id in {game.court_id() for game in self.games}}

        delete_keys = list()
        for game_id in self.games_dict:
            if game_id not in self.reports_dict:
                delete_keys.append(game_id)
        for game_id in delete_keys:
            self.games_dict.pop(game_id)
            p = None
            for n, game in enumerate(self.games):
                if game['game_id']==game_id:
                    p = n
                    break
            self.games.pop(p)

        self.games_counted = dict() # game_id -> data
        for game in self.games:
            counted = dict()
            if len(self.reports_dict[game.game_id()])<=game.capacity():
                counted['ideal_income'] = game.capacity()*game.cost()
            else:
                counted['ideal_income'] = len(self.reports_dict[game.game_id()])*game.cost()
            counted['empty'] = game.capacity()-len(self.reports_dict[game.game_id()])
            if counted['empty']<0: counted['empty']=0
            counted['lost_empty'] = counted['empty']*game.cost()
            counted['notvisited'] = len(list(filter(lambda x: x['status']==0, self.reports_dict[game.game_id()])))
            counted['lost_notvisited'] = counted['notvisited']*game.cost()
            counted['notpayed'] = len(list(filter(lambda x: x['status']==1, self.reports_dict[game.game_id()])))
            counted['lost_notpayed'] = counted['notpayed']*game.cost()
            counted['playedpayed'] = len(list(filter(lambda x: x['status']==2, self.reports_dict[game.game_id()])))
            counted['real_income'] = counted['playedpayed']*game.cost()
            counted['rent_charges'] = self.courts_dict[game.court_id()].cost()*(game.duration()/60)
            if game.game_id() in self.additional_charges_dict:
                counted['additional_charges'] = sum([i['cost'] for i in self.additional_charges_dict[game.game_id()]])
            else:
                counted['additional_charges'] = 0
            counted['profit'] = counted['real_income']-counted['rent_charges']-counted['additional_charges']

            self.games_counted[game.game_id()] = counted

        def sumgames(attr:str) -> int:
            return sum(map(lambda x: self.games_counted[x.game_id()][attr], self.games))



        self.ideal_income = sumgames('ideal_income')
        #self.ideal_income += sum([len(self.reports_dict[game['game_id']])*game['cost'] for game in self.games if game['capacity']<0])

        self.played_users = list(filter(lambda x: x['status']==2, self.reports))
        self.played_unique = {i['user_id'] for i in self.played_users if i['user_id']!=0}

        self.empty = sumgames('empty')
        self.lost_empty = sumgames('lost_empty')

        self.notvisited = sumgames('notvisited')
        self.lost_notvisited = sumgames('lost_notvisited')

        self.notpayed = sumgames('notpayed')
        self.lost_notpayed = sumgames('lost_notpayed')

        self.real_income = sumgames('real_income')
        self.rent_charges = sumgames('rent_charges')
        self.additional_charges = sumgames('additional_charges')

        self.profit = sumgames('profit')

        self.sport_games = dict() # sport_type -> [game_id]
        for game in self.games:
            if game.sport_type() not in self.sport_games:
                self.sport_games[game.sport_type()] = [game.game_id()]
            else:
                self.sport_games[game.sport_type()].append(game.game_id())

        self.sport_money = dict()
        for sport_id in self.sport_games:
            self.sport_money[sport_id] = sum([self.games_counted[game_id]['profit'] for game_id in self.sport_games[sport_id]])

        finances = db.execute("SELECT * FROM salary", dbutils.dbfields['salary'])
        finances_by_user = dict() # user_id -> [finance]
        for fin in finances:
            if fin['user_id'] not in finances_by_user:
                finances_by_user[fin['user_id']] = [fin]
            else:
                finances_by_user[fin['user_id']].append(fin)

        self.user_salary = dict()
        for user_id in finances_by_user:
            self.user_salary[user_id] = sum([self.sport_money[fin['sport_id']]*(fin['percents']/100) for fin in finances_by_user[user_id] if fin['sport_id'] in self.sport_money])


    def dict(self) -> dict:
        return {i:self.__dict__[i] for i in self.__dict__ if not i.startswith('_')}


class NewFinances:
    @staticmethod
    def percents(n:int, mx:int, digits:int=1) -> int:
        return round((n/mx)*100, digits) if mx!=0 else 0

    def __init__(self, game_finances_list:list, db:dbutils.DBConnection):
        self.games = game_finances_list
        self.games_dict = {game.game_id():game for game in self.games}
        self.sports = {sport.sport_id():sport for sport in sport_types.get(0, dbconnection=db)}
        self.real_games = db.execute("SELECT * FROM games WHERE game_id IN ({})".format(
            ', '.join(list(map(str, self.games_dict.keys())))), dbutils.dbfields['games'])
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

        db.execute("SELECT * FROM responsible_games_salary WHERE game_id IN ({})".format(
            ', '.join([str(game.game_id()) for game in self.games])), dbutils.dbfields['responsible_games_salary'])
        self.salary = group(lambda x: x['user_id'], db.last())
        self.users_get = users.get

        self.sport_games = group(lambda x: x.sport_id(), self.games)

        self.sport_money = dict()
        for sport_id in self.sport_games:
            self.sport_money[sport_id] = sum([game.real_profit() for game in self.sport_games[sport_id]])

        finances = db.execute("SELECT * FROM salary", dbutils.dbfields['salary'])
        finances_by_user = group(lambda x: x['user_id'], finances)

        self.user_salary = dict()
        for user_id in finances_by_user:
            self.user_salary[user_id] = sum([self.sport_money[fin['sport_id']]*(fin['percents']/100) for fin in finances_by_user[user_id] if fin['sport_id'] in self.sport_money])
        #for user_id in self.game_by_responsible:
        #    if user_id in self.user_salary:
        #        self.user_salary[user_id] += sum([game.responsible_salary() for game in self.game_by_responsible[user_id]])

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

    finances['profit'] = finances['real_income']-finances['rent_charges']-finances['additional_charges']

    dbconnection.execute("SELECT percents FROM responsible_salary WHERE user_id={}".format(game.responsible_user_id()))
    finances['responsible_salary'] = 0
    if len(dbconnection.last())>0 and finances['profit']>0:
        finances['responsible_salary'] = round(finances['profit']*(dbconnection.last()[0][0]/100))

    finances['real_profit'] = finances['profit'] - finances['responsible_salary']

    return finances

@autodb
def add_game_finances(game_id:int, dbconnection:dbutils.DBConnection=None):
    finances = calc_game(game_id, dbconnection=dbconnection)
    sql = "INSERT INTO finances VALUES ({})".format(', '.join(["'{}'".format(finances[i]) for i in dbutils.dbfields['finances']]))
    dbconnection.execute(sql)
    dbconnection.execute("SELECT percents FROM responsible_salary WHERE user_id={}".format(finances['responsible_user_id']))
    if finances['profit']>0 and len(dbconnection.last())>0:
        percents = dbconnection.last()[0][0]
        dbconnection.execute("INSERT INTO responsible_games_salary VALUES ({}, {}, {}, {}, {})".format(
            finances['responsible_user_id'], game_id, finances['profit'], percents, finances['responsible_salary']))

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
        'NOW()' if month==0 else month,
        'NOW()' if year==0 else year), dbutils.dbfields['finances'])
    return list(map(lambda x: GameFinance(x, dbconnection), dbconnection.last()))

@autodb
def get_current_month(dbconnection:dbutils.DBConnection=None) -> GameFinance:
    return get_by_date(dbconnection=dbconnection)

@autodb
def get_additional_charges(game_id:int, dbconnection:dbutils.DBConnection=None) -> list:
    dbconnection.execute("SELECT * FROM additional_charges WHERE game_id={}".format(game_id), dbutils.dbfields['additional_charges'])
    return dbconnection.last()