import dbutils
from models import sport_types
from objects import Game, Court


class Finances:
    @staticmethod
    def percents(n:int, mx:int, digits:int=1) -> int:
        return round((n/mx)*100, digits) if mx!=0 else 0

    def __init__(self, month:int, db:dbutils.DBConnection):
        self._db = db

        if month==0:
            month = 'MONTH(NOW())'

        self.games = db.execute("SELECT * FROM games WHERE "
                               "MONTH(datetime)={} AND "
                               "datetime+INTERVAL duration MINUTE<NOW() AND "
                               "capacity>0 AND deleted=0 AND "
                               "game_id IN (SELECT game_id FROM reports) ORDER BY datetime DESC".format(month), dbutils.dbfields['games'])
        self.games = list(map(lambda x: Game(x, dbconnection=db), self.games))
        self.games_dict = {game.game_id():game for game in self.games}

        self.reports = db.execute("SELECT * FROM reports WHERE game_id IN ({})".format(', '.join(map(str, self.games_dict))),
                     dbutils.dbfields['reports']) if len(self.games)>0 else list()
        self.reports_dict = dict()
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
            counted['empty'] = game.capacity()-len(list(filter(lambda x: x['status']>=0 and x['user_id']!=0, self.reports_dict[game.game_id()])))
            if counted['empty']<0: counted['empty']=0
            counted['lost_empty'] = counted['empty']*game.cost()
            counted['notvisited'] = len(list(filter(lambda x: x['status']==0, self.reports_dict[game.game_id()])))
            counted['lost_notvisited'] = counted['notvisited']*game.cost()
            counted['notpayed'] = len(list(filter(lambda x: x['status']==1, self.reports_dict[game.game_id()])))
            counted['lost_notpayed'] = counted['notpayed']*game.cost()
            counted['playedpayed'] = len(list(filter(lambda x: x['status']==2, self.reports_dict[game.game_id()])))
            counted['real_income'] = counted['playedpayed']*game.cost()
            counted['rent_charges'] = self.courts_dict[game.court_id()].cost()*(game.duration()/60)
            counted['profit'] = counted['real_income']-counted['rent_charges']

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