import json
import dbutils

from objects.mydatetime import GameDateTime, DateTime, UserAge, UserLastTime
import models
import pages

class City:
    def __init__(self, city:dict):
        self._city = city

    def city_id(self) -> int:
        return self._city['city_id']

    def title(self) -> str:
        return self._city['title']

    def geopoint(self) -> str:
        return self._city['geopoint']

    def __bool__(self): return True

    def __len__(self): return 1


class Report:
    def __init__(self, report:dict):
        self._report = report

    def reported(self) -> bool:
        return self._report['reported']

    def __getitem__(self, item):
        return self._report[item]

        # TODO: Report rework


class SportType:
    def __init__(self, sport_type:dict):
        self._sport_type = sport_type

    def sport_id(self) -> int:
        return self._sport_type['sport_id']

    def title(self) -> str:
        return self._sport_type['title']

    def __bool__(self): return True

    def __len__(self): return 1


class CourtType:
    def __init__(self, court_type:dict):
        self._court_type = court_type

    def type_id(self) -> int:
        return self._court_type['type_id']

    def title(self) -> str:
        return self._court_type['title']


class GameType:
    def __init__(self, game_type:dict, dbconnection:dbutils.DBConnection=None):
        self._game_type = game_type
        self._db = dbconnection

    def type_id(self) -> int:
        return self._game_type['type_id']

    def sport_type(self, detalized:bool=False) -> SportType:
        if not detalized:
            if isinstance(self._game_type['sport_type'], SportType):
                return self._game_type['sport_type'].sport_id()
            else:
                return self._game_type['sport_type']
        if not isinstance(self._game_type['sport_type'], SportType):
            self._game_type['sport_type'] = sport_types.get(self._game_type['sport_type'], dbconnection=self._db)
        return self._game_type['sport_type']

    def title(self) -> str:
        return self._game_type['title']

    def __bool__(self):
        return True

    def __len__(self):
        return 1


class Command:
    def __init__(self, command:dict, dbconnection:dbutils.DBConnection=None):
        self._command = command
        self._db = dbconnection

    def command_id(self) -> int:
        return self._command['command_id']

    def title(self) -> str:
        return self._command['title']

    def game_id(self, detalized:bool=False):
        if not detalized:
            if isinstance(self._command['game_id'], Game):
                return self._command['game_id'].game_id()
            else:
                return self._command['game_id']
        if not isinstance(self._command['game_id'], Game):
            self._command['game_id'] = games.get_by_id(self._command['game_id'], dbconnection=self._db)
        return self._command['game_id']

    def commander_id(self, detalized:bool=False):
        if not detalized:
            if isinstance(self._command['commander_id'], User):
                return self._command['commander_id'].user_id()
            else:
                return self._command['commander_id']
        if not isinstance(self._command['commander_id'], User):
            self._command['commander_id'] = users.get(self._command['commander_id'], dbconnection=self._db)
        return self._command['commander_id']

    def subscribed(self, detalized:bool=False) -> list:
        if 'subscribed' not in self._command: self._command['subscribed'] = commands.get_subscribed(self.command_id(), dbconnection=self._db)
        if len(self._command['subscribed']) == 0: return list()

        if not detalized:
            if isinstance(self._command['subscribed'][0], User):
                return list(map(lambda x: x.user_id(), self._command['subscribed']))
            else:
                return self._command['subscribed']
        if not isinstance(self._command['subscribed'][0], User):
            self._command['subscribed'] = users.get(self._command['subscribed'],
                                              count=slice(0, len(self._command['subscribed'])), dbconnection=self._db)
        return self._command['subscribed']

class Amplua:
    def __init__(self, amplua:dict, dbconnection:dbutils.DBConnection=None):
        self._amplua = amplua
        self._db = dbconnection

    def amplua_id(self) -> int:
        return self._amplua['amplua_id']

    def sport_type(self, detalized:bool=False) -> SportType:
        if not detalized:
            if isinstance(self._amplua['sport_type'], SportType):
                return self._amplua['sport_type'].sport_id()
            else:
                return self._amplua['sport_type']
        if not isinstance(self._amplua['sport_type'], SportType):
            self._amplua['sport_type'] = sport_types.get(self._amplua['sport_type'], dbconnection=self._db)
        return self._amplua['sport_type']

    def title(self) -> str:
        return self._amplua['title']

    def __bool__(self):
        return True

    def __len__(self):
        return 1


class Court:
    def __init__(self, court:dict, dbconnection:dbutils.DBConnection=None):
        self._court = court
        self._court['sport_types'] = list(map(int, self._court['sport_types'].split(',')))
        self._db = dbconnection

    def city_id(self, detalized:bool=False) -> City:
        if not detalized:
            if isinstance(self._court['city_id'], City):
                return self._court['city_id'].city_id()
            else:
                return self._court['city_id']
        if not isinstance(self._court['city_id'], City):
            self._court['city_id'] = cities.get(self._court['city_id'], dbconnection=self._db)
        return self._court['city_id']

    def sport_types(self, detalized:bool=False) -> list:
        if len(self._court['sport_types']) == 0: return list()
        if not detalized:
            if isinstance(self._court['sport_types'][0], SportType):
                return list(map(lambda x: x.sport_id(), self._court['sport_types']))
            else:
                return self._court['sport_types']
        if not isinstance(self._court['sport_types'][0], SportType):
            self._court['sport_types'] = sport_types.get(self._court['sport_types'], dbconnection=self._db)
        return self._court['sport_types']

    def nearest_game(self): # TODO: definition
        if 'nearest_game' in self._court: return self._court['nearest_game']
        self._court['nearest_game'] = games.get_recent(court_id=self.court_id(),
                                                       city_id=self.city_id(),
                                                       count=slice(0, 1),
                                                       dbconnection=self._db)
        if len(self._court['nearest_game']) > 0:
            self._court['nearest_game'] = self._court['nearest_game'][0]
        else:
            self._court['nearest_game'] = None
        return self._court['nearest_game']

    def type(self, detalized:bool=False) -> CourtType:
        if not detalized:
            if isinstance(self._court['type'], CourtType):
                return self._court['type'].type_id()
            else:
                return self._court['type']
        if not isinstance(self._court['type'], CourtType):
            self._court['type'] = court_types.get(self._court['type'], dbconnection=self._db)
        return self._court['type']

    def court_id(self) -> int:
        return self._court['court_id']

    def title(self) -> str:
        return self._court['title']

    def description(self) -> str:
        return self._court['description']

    def address(self) -> str:
        return self._court['address']

    def geopoint(self) -> str:
        return self._court['geopoint']

    def worktime(self) -> str:
        return self._court['worktime']

    def cost(self) -> int:
        return self._court['cost']

    def cover(self) -> str:
        return self._court['cover']

    def infrastructure(self) -> str:
        return self._court['infrastructure']

    def phone(self) -> str:
        return self._court['phone']

    def max_players(self) -> int:
        return self._court['max_players']

    def __bool__(self):
        return True

    def __len__(self):
        return 1


class _UserName:
    def __init__(self, first_name:str, middle_name:str, last_name:str):
        self._first_name = first_name
        self._last_name = last_name
        self._middle_name = middle_name

    def first(self) -> str:
        return self._first_name

    def last(self) -> str:
        return self._last_name

    def middle(self) -> str:
        return self._middle_name

    def __str__(self):
        return self.first() + ' ' + self.last()


class _UserLevel:
    def __init__(self, userlevel:str):
        self._userlevel = set(map(int, models.decode_set(userlevel)))

    def admin(self) -> bool:
        return 0 in self

    def organizer(self) -> bool:
        return 1 in self

    def responsible(self) -> bool:
        return 2 in self

    def common(self) -> bool:
        return 3 in self or self.responsible() or self.organizer() or self.admin()

    def resporgadmin(self) -> bool:
        return self.admin() or self.organizer() or self.responsible()

    def judge(self) -> bool:
        return 4 in self

    def max(self) -> int:
        for n, i in enumerate(range(5)):
            if i in self:
                return n

    def __contains__(self, item):
        return item in self._userlevel


class _UserSettings:
    def __init__(self, settings:str):
        self._settings = json.loads(settings)

    def send_mail(self) -> bool:
        return self._settings['send_mail']

    def show_phone(self) -> bool:
        return self._settings['show_phone'] == 'all'


class User:
    def __init__(self, user:dict, dbconnection:dbutils.DBConnection=None):
        self._user = user
        self._db = dbconnection

        self.name = _UserName(self._user['first_name'], self._user['middle_name'], self._user['last_name'])
        self.bdate = UserAge(self._user['bdate'])
        self.regdate = DateTime(self._user['regdate'])
        self.lasttime = UserLastTime(self._user['lasttime'])
        self.userlevel = _UserLevel(self._user['userlevel'])
        self.settings = _UserSettings(self._user['settings'])
        self._user['ampluas'] = list(map(int, models.decode_set(self._user['ampluas'])))

    def ampluas(self, detalized:bool=False) -> list:
        if len(self._user['ampluas']) == 0: return list()
        if not detalized:
            if isinstance(self._user['ampluas'][0], Amplua):
                return list(map(lambda x: x.amplua_id(), self._user['ampluas']))
            else:
                return self._user['ampluas']
        if not isinstance(self._user['ampluas'][0], Amplua):
            self._user['ampluas'] = ampluas.get(self._user['ampluas'], dbconnection=self._db)
        return self._user['ampluas']

    def friends(self, detalized:bool=False) -> list:
        if 'friends' not in self._user: self._user['friends'] = users.get_friends(self.user_id(), dbconnection=self._db)
        if len(self._user['friends']) == 0: return list()

        if not detalized:
            if isinstance(self._user['friends'][0], User):
                return list(map(lambda x: x.user_id(), self._user['friends']))
            else:
                return self._user['friends']
        if not isinstance(self._user['friends'][0], User):
            self._user['friends'] = users.get(self._user['friends'],
                                              count=slice(0, len(self._user['friends'])), dbconnection=self._db)
        return self._user['friends']

    def city_id(self, detalized:bool=False) -> City:
        if not detalized:
            if isinstance(self._user['city_id'], City):
                return self._user['city_id'].city_id()
            else:
                return self._user['city_id']
        if not isinstance(self._user['city_id'], City):
            self._user['city_id'] = cities.get(self._user['city_id'], dbconnection=self._db)
        return self._user['city_id']

    def gameinfo(self) -> dict:
        if 'gameinfo' in self._user: return self._user['gameinfo']
        self._user['gameinfo'] = usergames.get_game_stats(self.user_id(), dbconnection=self._db)
        return self._user['gameinfo']

    def activated(self) -> bool:
        return bool(self._user['activated'])

    def banned(self) -> bool:
        if 'banned' not in self._user: self._user['banned'] = ban.banned(self.user_id(), dbconnection=self._db)
        return self._user['banned']

    def email(self) -> str:
        return self._user['email']

    def user_id(self) -> int:
        return self._user['user_id']

    def height(self) -> int:
        return self._user['height']

    def passwd(self) -> str:
        return self._user['passwd']

    def weight(self) -> int:
        return self._user['weight']

    def sex(self) -> str:
        return self._user['sex']

    def vkuserid(self) -> int:
        return self._user['vkuserid']

    def phone(self) -> str:
        return self._user['phone']

    def closedb(self):
        self._db.close()

    def __bool__(self):
        return True

    def __len__(self):
        return 1



class Game:
    def __init__(self, game:dict, dbconnection:dbutils.DBConnection=None):
        self._game = game
        self._db = dbconnection
        self.datetime = GameDateTime(self._game['datetime'], self)
        self.report = Report(json.loads(self._game['report']))

    def city_id(self, detalized:bool=False) -> City:
        if not detalized:
            if isinstance(self._game['city_id'], City):
                return self._game['city_id'].city_id()
            else:
                return self._game['city_id']
        if not isinstance(self._game['city_id'], City):
            self._game['city_id'] = cities.get(self._game['city_id'], dbconnection=self._db)
        return self._game['city_id']

    def game_type(self, detalized:bool=False) -> GameType:
        if not detalized:
            if isinstance(self._game['game_type'], GameType):
                return self._game['game_type'].type_id()
            else:
                return self._game['game_type']
        if not isinstance(self._game['game_type'], GameType):
            self._game['game_type'] = game_types.get(self._game['game_type'], dbconnection=self._db)
        return self._game['game_type']

    def sport_type(self, detalized:bool=False) -> SportType:
        if not detalized:
            if isinstance(self._game['sport_type'], SportType):
                return self._game['sport_type'].sport_id()
            else:
                return self._game['sport_type']
        if not isinstance(self._game['sport_type'], SportType):
            self._game['sport_type'] = sport_types.get(self._game['sport_type'], dbconnection=self._db)
        return self._game['sport_type']

    def court_id(self, detalized:bool=False) -> Court:
        if not detalized:
            if isinstance(self._game['court_id'], Court):
                return self._game['court_id'].court_id()
            else:
                return self._game['court_id']
        if not isinstance(self._game['court_id'], Court):
            self._game['court_id'] = courts.get(self._game['court_id'], dbconnection=self._db)
        return self._game['court_id']

    def responsible_user_id(self, detalized:bool=False) -> User:
        if not detalized:
            if isinstance(self._game['responsible_user_id'], User):
                return self._game['responsible_user_id'].user_id()
            else:
                return self._game['responsible_user_id']
        if not isinstance(self._game['responsible_user_id'], User):
            self._game['responsible_user_id'] = users.get(self._game['responsible_user_id'], dbconnection=self._db)
        return self._game['responsible_user_id']

    def subscribed(self, detalized:bool=False) -> list:
        if 'subscribed' not in self._game: self._game['subscribed'] = games.get_subscribed_to_game(self.game_id(),
                                                                                                   dbconnection=self._db)
        if len(self._game['subscribed']) == 0: return list()

        if not detalized:
            if isinstance(self._game['subscribed'][0], User):
                return list(map(lambda x: x.user_id(), self._game['subscribed']))
            else:
                return self._game['subscribed']
        if not isinstance(self._game['subscribed'][0], User):
            self._game['subscribed'] = users.get(self._game['subscribed'], dbconnection=self._db)
        return self._game['subscribed']

    def reserved(self, detalized:bool=False) -> User:
        if isinstance(self._game['reserved'], int) and self._game['reserved']==0: return list()
        if not isinstance(self._game['reserved'], list): self._game['reserved'] = games.get_reserved_to_game(self.game_id(), dbconnection=self._db)
        if len(self._game['reserved'])==0: return list()

        if not detalized:
            if isinstance(self._game['reserved'][0], User):
                return list(map(lambda x: x.user_id(), self._game['reserved']))
            else:
                return self._game['reserved']
        if not isinstance(self._game['reserved'][0], User):
            self._game['reserved'] = users.get(self._game['reserved'], dbconnection=self._db)
        return self._game['reserved']

    def created_by(self, detalized:bool=False) -> User:
        if not detalized:
            if isinstance(self._game['created_by'], User):
                return self._game['created_by'].user_id()
            else:
                return self._game['created_by']
        if not isinstance(self._game['created_by'], User):
            self._game['created_by'] = users.get(self._game['created_by'], dbconnection=self._db)
        return self._game['created_by']

    def is_subscribed(self) -> bool:
        return pages.auth.loggedin() and pages.auth.current().user_id() in set(self.subscribed())

    def command_game(self) -> bool:
        return bool(self._game['command_game'])

    def commands(self, detalized:bool=False) -> list:
        if not self.command_game(): return list()
        if 'commands' not in self._game: self._game['commands'] = commands.get_command_ids(self.game_id(), dbconnection=self._db)
        if len(self._game['commands']) == 0: return list()

        if not detalized:
            if isinstance(self._game['commands'][0], Command):
                return list(map(lambda x: x.user_id(), self._game['commands']))
            else:
                return self._game['commands']
        if not isinstance(self._game['commands'][0], Command):
            self._game['commands'] = commands.get_commands(self._game['commands'], dbconnection=self._db)
        return self._game['commands']

    def can_subscribe(self) -> bool:
        return self.datetime.can_subscribe

    def description(self) -> str:
        return self._game['description']

    def game_id(self) -> int:
        return self._game['game_id']

    def duration(self) -> int:
        return self._game['duration']

    def cost(self) -> int:
        return self._game['cost']

    def capacity(self) -> int:
        return self._game['capacity']

    def __bool__(self):
        return True

    def __len__(self):
        return 1


class Notification:
    def __init__(self, notification:dict, dbconnection:dbutils.DBConnection=None):
        self._notification = notification
        self.datetime = DateTime(self._notification['datetime'])
        self._db = dbconnection

    def notification_id(self) -> int:
        return self._notification['notification_id']

    def user_id(self, detalized:bool=False):
        if not detalized:
            if isinstance(self._notification['user_id'], User):
                return self._notification['user_id'].user_id()
            else:
                return self._notification['user_id']
        if not isinstance(self._notification['user_id'], User):
            self._notification['user_id'] = users.get(self._notification['user_id'], dbconnection=self._db)
        return self._notification['user_id']

    def text(self) -> str:
        return self._notification['text']

    def read(self) -> bool:
        return bool(self._notification['read'])

    def level(self) -> int:
        return self._notification['level']

    def game_id(self, detalized:bool=False) -> Game:
        if not detalized:
            if isinstance(self._notification['game_id'], Game):
                return self._notification['game_id'].game_id()
            else:
                return self._notification['game_id']
        if not isinstance(self._notification['game_id'], Game):
            self._notification['game_id'] = games.get_by_id(self._notification['game_id'], dbconnection=self._db)
        return self._notification['game_id']

    def type(self) -> int:
        return self._notification['type']

    def __bool__(self):
        return True

    def __len__(self):
        return 1

import models.sport_types as sport_types
import models.cities as cities
import models.game_types as game_types
import models.games as games
import models.courts as courts
import models.users as users
import models.ampluas as ampluas
import models.usergames as usergames
import models.ban as ban
import models.commands as commands
import models.court_types as court_types