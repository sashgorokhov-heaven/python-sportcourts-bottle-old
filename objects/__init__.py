import base64
import json
import datetime

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


class SeoInfo:
    def __init__(self, seoinfo:dict):
        self._seoinfo = seoinfo

    def tplname(self) -> str:
        return self._seoinfo['tplname']

    def keywords(self) -> str:
        return self._seoinfo['keywords']

    def description(self) -> str:
        return self._seoinfo['description']


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


class Outlay:
    def __init__(self, outlay:dict):
        self._outlay = outlay

    def id(self) -> int:
        return self._outlay['id']

    def datetime(self) -> datetime.datetime:
        return self._outlay['datetime']

    def title(self) -> str:
        return self._outlay['title']

    def description(self) -> str:
        return self._outlay['description']

    def cost(self) -> int:
        return self._outlay['cost']


class Comand:
    def __init__(self, comand:dict, dbconnection:dbutils.DBConnection=None):
        self._comand = comand
        self._db = dbconnection

    def comand_id(self) -> int:
        return self._comand['comand_id']

    def title(self) -> str:
        return self._comand['title']

    def game_id(self, detalized:bool=False):
        if not detalized:
            if isinstance(self._comand['game_id'], Game):
                return self._comand['game_id'].game_id()
            else:
                return self._comand['game_id']
        if not isinstance(self._comand['game_id'], Game):
            self._comand['game_id'] = games.get_by_id(self._comand['game_id'], dbconnection=self._db)
        return self._comand['game_id']

    def comander_id(self, detalized:bool=False):
        if not detalized:
            if isinstance(self._comand['comander_id'], User):
                return self._comand['comander_id'].user_id()
            else:
                return self._comand['comander_id']
        if not isinstance(self._comand['comander_id'], User):
            self._comand['comander_id'] = users.get(self._comand['comander_id'], dbconnection=self._db)
        return self._comand['comander_id']

    def subscribed(self, detalized:bool=False) -> list:
        if 'subscribed' not in self._comand: self._comand['subscribed'] = comands.get_subscribed(self.comand_id(),
                                                                                                 dbconnection=self._db)
        if len(self._comand['subscribed']) == 0: return list()

        if not detalized:
            if isinstance(self._comand['subscribed'][0], User):
                return list(map(lambda x: x.user_id(), self._comand['subscribed']))
            else:
                return self._comand['subscribed']
        if not isinstance(self._comand['subscribed'][0], User):
            self._comand['subscribed'] = users.get(self._comand['subscribed'],
                                                   count=slice(0, len(self._comand['subscribed'])),
                                                   dbconnection=self._db)
        return self._comand['subscribed']


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


class Tag:
    def __init__(self, tag:dict):
        self._tag = tag

    def tag_id(self) -> int:
        return self._tag['tag_id']

    def title(self) -> str:
        return self._tag['title']

    def description(self) -> str:
        return self._tag['description']

    def keywords(self) -> str:
        return self._tag['keywords']

    def general_description(self) -> str:
        return self._tag['general_description']


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

    def nearest_game(self):  # TODO: definition
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

    def admin_description(self) -> str:
        return self._court['admin_description']

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
    def __init__(self, first_name:str, last_name:str):
        self._first_name = first_name
        self._last_name = last_name

    def first(self) -> str:
        return self._first_name

    def last(self) -> str:
        return self._last_name

    #def middle(self) -> str:
    #    return self._middle_name

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

    def writer(self) -> bool:
        return 4 in self or self.admin()

    def moderator(self) -> bool:
        return 5 in self or self.writer() or self.admin()

    def resporgadmin(self) -> bool:
        return self.admin() or self.organizer() or self.responsible()

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

        self._pure = user.copy()

        self.name = _UserName(self._user['first_name'], self._user['last_name'])
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
            self._user['friends'] = users.get(self._user['friends'], count=slice(0, len(self._user['friends'])),
                                              dbconnection=self._db)
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
        self._user['gameinfo'] = games.get_game_stats(self.user_id(), dbconnection=self._db)
        return self._user['gameinfo']

    #def activated(self) -> bool:
    #    return bool(self._user['activated'])

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

    def played_games(self) -> int:
        return self._user['played_games']

    def closedb(self):
        self._db.close()

    def __bool__(self):
        return True

    def __len__(self):
        return 1


class GameFinance:
    def __init__(self, finance:dict, dbconnection:dbutils.DBConnection=None):
        self._finance = finance
        self._db = dbconnection
        self.datetime = DateTime(self._finance['datetime'])

    def game_id(self) -> int:
        return self._finance['game_id']

    def capacity(self) -> int:
        return self._finance['capacity']

    def cost(self) -> int:
        return self._finance['cost']

    def sport_id(self, detalized:bool=False) -> SportType:
        if not detalized:
            if isinstance(self._finance['sport_id'], SportType):
                return self._finance['sport_id'].sport_id()
            else:
                return self._finance['sport_id']
        if not isinstance(self._finance['sport_id'], SportType):
            self._finance['sport_id'] = sport_types.get(self._finance['sport_id'], dbconnection=self._db)
        return self._finance['sport_id']

    def responsible_user_id(self, detalized:bool=False) -> User:
        if not detalized:
            if isinstance(self._finance['responsible_user_id'], User):
                return self._finance['responsible_user_id'].user_id()
            else:
                return self._finance['responsible_user_id']
        if not isinstance(self._finance['responsible_user_id'], User):
            self._finance['responsible_user_id'] = users.get(self._finance['responsible_user_id'], dbconnection=self._db)
        return self._finance['responsible_user_id']

    def created_by(self, detalized:bool=False) -> User:
        if not detalized:
            if isinstance(self._finance['created_by'], User):
                return self._finance['created_by'].user_id()
            else:
                return self._finance['created_by']
        if not isinstance(self._finance['created_by'], User):
            self._finance['created_by'] = users.get(self._finance['created_by'], dbconnection=self._db)
        return self._finance['created_by']

    def visited(self) -> int:
        return self._finance['visited']

    def empty(self) -> int:
        return self._finance['empty']

    def lost_empty(self) -> int:
        return self._finance['lost_empty']

    def notvisited(self) -> int:
        return self._finance['notvisited']

    def lost_notvisited(self) -> int:
        return self._finance['lost_notvisited']

    def notpayed(self) -> int:
        return self._finance['notpayed']

    def lost_notpayed(self) -> int:
        return self._finance['lost_notpayed']

    def playedpayed(self) -> int:
        return self._finance['playedpayed']

    def real_income(self) -> int:
        return self._finance['real_income']

    def ideal_income(self) -> int:
        return self._finance['ideal_income']

    def rent_charges(self) -> float:
        return self._finance['rent_charges']

    def additional_charges(self, detalized:bool=False):
        if detalized:
            if '_additional_charges' not in self._finance:
                self._finance['_additional_charges'] = finances.get_additional_charges(self.game_id(), dbconnection=self._db)
            return self._finance['_additional_charges']
        return self._finance['additional_charges']

    def responsible_salary(self) -> int:
        return self._finance['responsible_salary']

    def profit(self) -> float:
        return self._finance['profit']

    def real_profit(self) -> int:
        return self._finance['real_profit']


class BlogPost:
    def __init__(self, blog_post:dict, dbconnection:dbutils.DBConnection=None):
        self._blog_post = blog_post
        self._db = dbconnection
        self.datetime = DateTime(self._blog_post['datetime'])

    def post_id(self) -> int:
        return self._blog_post['post_id']

    def status(self) -> bool:
        return bool(self._blog_post['status'])

    def keywords(self) -> str:
        return self._blog_post['keywords']

    def description(self) -> str:
        return self._blog_post['description']

    def title(self) -> str:
        return self._blog_post['title']

    def content(self) -> str:
        return base64.b64decode(self._blog_post['content']).decode()

    def created_by(self, detalized:bool) -> User:
        if not detalized:
            if isinstance(self._blog_post['created_by'], User):
                return self._blog_post['created_by'].user_id()
            else:
                return self._blog_post['created_by']
        if not isinstance(self._blog_post['created_by'], User):
            self._blog_post['created_by'] = users.get(self._blog_post['created_by'], dbconnection=self._db)
        return self._blog_post['created_by']

    def tags(self) -> list:
        if 'tags' not in self._blog_post:
            self._blog_post['tags'] = blog.get_tags(self.post_id(), dbconnection=self._db)
        return self._blog_post['tags']


class Game:
    def __init__(self, game:dict, dbconnection:dbutils.DBConnection=None):
        self._game = game
        self._db = dbconnection
        self.datetime = GameDateTime(self._game['datetime'], self)

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

    def reserved(self) -> int:
        return self._game['reserved']

    def reserved_people(self, detalized:bool=False) -> User:
        if self.reserved() == 0: return list()
        if 'reserved_people' not in self._game: self._game['reserved_people'] = games.get_reserved_to_game(
            self.game_id(), dbconnection=self._db)
        if len(self._game['reserved_people']) == 0: return list()

        if not detalized:
            if isinstance(self._game['reserved_people'][0], User):
                return list(map(lambda x: x.user_id(), self._game['reserved_people']))
            else:
                return self._game['reserved_people']
        if not isinstance(self._game['reserved_people'][0], User):
            self._game['reserved_people'] = users.get(self._game['reserved_people'], dbconnection=self._db)
        return self._game['reserved_people']

    def created_by(self, detalized:bool=False) -> User:
        if not detalized:
            if isinstance(self._game['created_by'], User):
                return self._game['created_by'].user_id()
            else:
                return self._game['created_by']
        if not isinstance(self._game['created_by'], User):
            self._game['created_by'] = users.get(self._game['created_by'], dbconnection=self._db)
        return self._game['created_by']

    def reported(self) -> bool:
        if 'reported' not in self._game: self._game['reported'] = reports.reported(self.game_id(), dbconnection=self._db)
        return self._game['reported']

    def report(self, detalized:bool=False) -> dict:
        if 'report' not in self._game: self._game['report'] = reports.get(self.game_id(), dbconnection=self._db)

        if detalized:
            if 'report_detalized' not in self._game:
                self._game['report_detalized'] = {'registered': dict(), 'unregistered': {name:self._game['report']['unregistered'][name] for name in self._game['report']['unregistered'] if self._game['report']['unregistered'][name][0]==2}}
                self._game['report_detalized']['registered'] = {
                    user.user_id():user for user in users.get(
                        list(map(lambda x: int(x), filter(lambda x: self._game['report']['registered'][x]==2, self._game['report']['registered']))),
                        count=slice(0, len(self._game['report']['registered'])),
                        dbconnection=self._db
                    )
                }
            total = len(self._game['report_detalized']['registered'])+len(self._game['report_detalized']['unregistered'])
            return self._game['report_detalized'], total

        return self._game['report']

    def deleted(self) -> bool:
        return bool(self._game['deleted'])

    def is_subscribed(self) -> bool:
        return pages.auth.loggedin() and pages.auth.current().user_id() in set(self.subscribed())

    def comand_game(self) -> bool:
        return bool(self._game['comand_game'])

    def comands(self, detalized:bool=False) -> list:
        if not self.comand_game(): return list()
        if 'comands' not in self._game: self._game['comands'] = comands.get_comand_ids(self.game_id(),
                                                                                       dbconnection=self._db)
        if len(self._game['comands']) == 0: return list()

        if not detalized:
            if isinstance(self._game['comands'][0], Comand):
                return list(map(lambda x: x.user_id(), self._game['comands']))
            else:
                return self._game['comands']
        if not isinstance(self._game['comands'][0], Comand):
            self._game['comands'] = comands.get_comands(self._game['comands'], dbconnection=self._db)
        return self._game['comands']

    def can_subscribe(self) -> bool:
        return self.datetime.can_subscribe

    def notificated(self) -> bool:
        return bool(self._game['notificated'])

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
import models.ban as ban
import models.comands as comands
import models.finances as finances
import models.court_types as court_types
import models.reports as reports
import models.blog as blog