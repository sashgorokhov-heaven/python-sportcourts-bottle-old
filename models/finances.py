import dbutils
from models import sport_types



class Finances:
    @staticmethod
    def percents(n:int, mx:int, digits:int=1) -> int:
        return round((n/mx)*100, digits)

    def __init__(self, month:int, db:dbutils.DBConnection):
        self._db = db

        if month==0:
            month = 'MONTH(NOW())'

        self.games = db.execute("SELECT * FROM games WHERE "
                               "MONTH(datetime)={} AND "
                               "datetime+INTERVAL duration MINUTE<NOW() AND "
                               "game_id IN (SELECT game_id FROM reports) ORDER BY datetime DESC".format(month), dbutils.dbfields['games'])
        self.games_dict = {game['game_id']:game for game in self.games}

        self.reports = db.execute("SELECT * FROM reports WHERE game_id IN ({})".format(', '.join(map(str, self.games_dict))),
                     dbutils.dbfields['reports'])
        self.reports_dict = dict()
        for report in self.reports:
            if report['game_id'] not in self.reports_dict:
                self.reports_dict[report['game_id']] = [report]
            else:
                self.reports_dict[report['game_id']].append(report)

        self.courts = db.execute("SELECT * FROM courts", dbutils.dbfields['courts'])
        self.courts_dict = {court['court_id']:court for court in self.courts}
        self.sports = {sport.sport_id():sport for sport in sport_types.get(0, dbconnection=db)}

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

        self.ideal_income = sum([game['capacity']*game['cost'] for game in self.games if game['capacity']>0])
        self.ideal_income += sum([len(self.reports_dict[game['game_id']])*game['cost'] for game in self.games if game['capacity']<0])

        self.played_users = list(filter(lambda x: x['status']==2, self.reports))
        self.played_unique = {i['user_id'] for i in self.played_users if i['user_id']!=0}

        self.empty = sum([game['capacity']-len(list(filter(lambda x: x['status']>=0 and x['user_id']!=0, self.reports_dict[game['game_id']]))) for game in self.games])
        self.lost_empty = sum([(game['capacity']-len(list(filter(lambda x: x['status']>=0 and x['user_id']!=0, self.reports_dict[game['game_id']]))))*game['cost'] for game in self.games])

        self.notvisited = sum([len(list(filter(lambda x: x['status']==0, self.reports_dict[game['game_id']]))) for game in self.games])
        self.lost_notvisited = sum([len(list(filter(lambda x: x['status']==0, self.reports_dict[game['game_id']])))*game['cost'] for game in self.games])

        self.notpayed = sum([len(list(filter(lambda x: x['status']==1, self.reports_dict[game['game_id']]))) for game in self.games])
        self.lost_notpayed = sum([len(list(filter(lambda x: x['status']==1, self.reports_dict[game['game_id']])))*game['cost'] for game in self.games])

        self.real_income = self.ideal_income-self.lost_empty-self.lost_notvisited-self.lost_notpayed
        self.rent_charges = sum([self.courts_dict[game['court_id']]['cost']*(game['duration']/60) for game in self.games])

        self.profit = self.real_income-self.rent_charges

        self.games_profit = {game['game_id']:len(list(filter(lambda x: x['status']==2, self.reports_dict[game['game_id']])))*game['cost']-self.courts_dict[game['court_id']]['cost']*(game['duration']/60) for game in self.games}

        self.sport_games = dict()
        for game in self.games:
            if game['sport_type'] not in self.sport_games:
                self.sport_games[game['sport_type']] = [game]
            else:
                self.sport_games[game['sport_type']].append(game)

        sport_money = dict()
        for sport_id in self.sport_games:
            sport_money[sport_id] = sum([self.games_profit[game['game_id']] for game in self.sport_games[sport_id]])

    def dict(self) -> dict:
        return {i:self.__dict__[i] for i in self.__dict__ if not i.startswith('_')}