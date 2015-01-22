import bottle
import datetime
import time
import itertools
import random
import pages
import dbutils
import json
from modules import logging, create_link, utils
from models import users, cities, ampluas, decode_set, courts, sport_types, game_types, court_types, games, notificating
from models import notifications


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)

def response(obj) -> str:
    return dump({'response':obj})

def error(obj) -> str:
    return dump({'error':obj})

def generate_token(length:int=20) -> str:
    return ''.join(random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))), length))


class Error(Exception):
    def __init__(self, code:int, description:str, e:Exception=None):
        self.code = code
        self.description = description
        self.e=e
        super().__init__(code, description, e)

    @staticmethod
    def unhandled(e:Exception):
        return Error(0, 'Unhandled exception', e)

    @staticmethod
    def lost_parameter(params:set):
        return Error(1, 'Lost parameters:{}'.format(','.join(params)))

    @staticmethod
    def invalid_auth():
        return Error(2, 'Invalid email or password')

    @staticmethod
    def invalid_token():
        return Error(3, 'Invalid token or token expired')

    @staticmethod
    def invalid_ip(ip:str):
        return Error(4, 'Invalid ip {}'.format(ip))

    @staticmethod
    def restricted_fields(fields:list):
        return Error(5, 'Restricted fields:{}'.format(','.join(fields)))

    @staticmethod
    def user_not_found(user_id:int):
        return Error(6, 'User <{}> not found'.format(user_id))

    @staticmethod
    def method_not_allowed():
        return Error(7, 'Method not allowed')

    @staticmethod
    def court_not_found(court_id:int):
        return Error(8, 'Court <{}> not found'.format(court_id))

    @staticmethod
    def unknown_field(field:str):
        return Error(9, 'Unknown field:{}'.format(field))

    @staticmethod
    def game_not_found(game_id:int):
        return Error(10, 'Game <{}> not found'.format(game_id))

    @staticmethod
    def game_conflict(conflict:int, data:str=None):
        return Error(11, 'Conflict <{}>{}'.format(conflict, (': '+str(data) if data else '')))

#    @staticmethod
#    def invalid_field(fields:list):
#        return Error(6, 'Invalid fields:{}'.format(','.join(fields)))

    def json(self) -> dict:
        ret = {'code':self.code, 'description':self.description}
        if self.e:
            ret['eclass'] = self.e.__class__.__name__
            ret['eargs'] = '{}'.format(','.join(list(map(str,self.e.args)))) if len(self.e.args)>0 else ''
        return ret


def required_param(*args):
    def decor(func):
        def wrapper(*args2, **kwargs2):
            d = set(args).difference({i for i in bottle.request.query})
            if len(d)>0:
                raise Error.lost_parameter(d)
            return func(*args2, **kwargs2)
        return wrapper
    return decor


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return response(func(*args, **kwargs))
        except Error as e:
            return error(e.json())
        except Exception as e:
            logging.error(e)
            return error(Error.unhandled(e).json())
    return wrapper


def check_auth(func):
    def wrapper(*args, **kwargs):
        token = bottle.request.query.get('token')
        with dbutils.dbopen() as db:
            au = db.execute("SELECT * FROM api_auth WHERE token='{}'".format(token), dbutils.dbfields['api_auth'])
            if len(au)>0:
                if bottle.request.remote_addr!=au[0]['ip']:
                    raise Error.invalid_ip(bottle.request.remote_addr)
                if datetime.datetime.now()-au[0]['datetime']>datetime.timedelta(days=7):
                    raise Error.invalid_token()
                return func(*args, **kwargs)
            raise Error.invalid_token()
    return required_param('token')(wrapper)


def handle_error_and_check_auth(func):
    return handle_error(check_auth(func))


def only_organizers(func):
    def wrapper(*args, **kwargs):
        with dbutils.dbopen() as db:
            user = current_user(db, True)
            if not user.userlevel.organizer():
                raise Error.method_not_allowed()
            return func(*args, **kwargs)
    return wrapper


def only_admins(func):
    def wrapper(*args, **kwargs):
        with dbutils.dbopen() as db:
            user = current_user(db, True)
            if not user.userlevel.admin():
                raise Error.method_not_allowed()
            return func(*args, **kwargs)
    return wrapper


def admins_and_organizers(func):
    def wrapper(*args, **kwargs):
        with dbutils.dbopen() as db:
            user = current_user(db, True)
            if not user.userlevel.admin() and not user.userlevel.organizer():
                raise Error.method_not_allowed()
            return func(*args, **kwargs)
    return wrapper


def strdatetime(d:dict) -> dict:
    for key in d:
        if isinstance(d[key], (datetime.datetime, datetime.date, datetime.time)):
            d[key] = str(d[key])
    return d


def current_user(db:dbutils.DBConnection, detalized:bool=False):
    token = bottle.request.query.get('token')
    user_id = db.execute("SELECT user_id FROM api_auth WHERE token='{}'".format(token))[0][0]
    if detalized:
        return users.get(user_id, dbconnection=db)
    return user_id


_available_fields = {
    "users_get": {
        "restricted": {'email', 'passwd', 'referer'}
    },
    "courts_get": {
        "restricted": {'cost', 'phone', 'admin_description'}
    },
    "games_get": {
        "restricted": {'notificated'}
    }
}


class getters:
    @staticmethod
    def city(city_id:int, db:dbutils.DBConnection) -> dict:
        city = cities.get(city_id, dbconnection=db)
        return {"city_id": city.city_id(), "title": city.title(), "geopoint": city.geopoint()}

    @staticmethod
    def court(court_id:int, db:dbutils.DBConnection) -> dict:
        court = courts.get(court_id, dbconnection=db)
        if len(court)==0: return None
        court_dict = court._court.copy()
        keys = set(court_dict.keys())
        keys.difference_update(_available_fields['courts_get']['restricted'])
        court_dict = {key:court_dict[key] for key in keys}
        formatters.court(court_dict, db)
        return court_dict

    @staticmethod
    def sport_type(sport_id:int, db:dbutils.DBConnection) -> dict:
        return sport_types.get(sport_id, dbconnection=db)._sport_type

    @staticmethod
    def game_type(type_int:int, db:dbutils.DBConnection) -> dict:
        return game_types.get(type_int, dbconnection=db)._game_type

    @staticmethod
    def user(user_id:int, db:dbutils.DBConnection) -> dict:
        user = db.execute("SELECT * FROM users WHERE user_id={}".format(user_id), dbutils.dbfields['users'])
        if len(user)==0: return None
        else: user = user[0]
        keys = set(user.keys())
        keys.difference_update(_available_fields['users_get']['restricted'])
        user_dict = {key:user[key] for key in keys}
        formatters.user(user_dict, db)
        return user_dict

    @staticmethod
    def amplua(ampluas_str:str, db:dbutils.DBConnection) -> list:
        amp = ampluas.get(decode_set(ampluas_str), dbconnection=db)
        return [{"amplua_id":a.amplua_id(), "sport_type":a.sport_type(), "title":a.title()} for a in amp]


class formatters:
    @staticmethod
    def user(user_dict:dict, db:dbutils.DBConnection):
        if 'city_id' in user_dict:
            user_dict['city'] = getters.city(user_dict['city_id'], db)
        if 'userlevel' in user_dict:
            user_dict['userlevel'] = list(map(int, user_dict['userlevel'].split('|')[1:-1]))
        if 'ampluas' in user_dict:
            user_dict['ampluas'] = getters.amplua(user_dict['ampluas'], db)
        if 'settings' in user_dict:
            user_dict['settings'] = json.loads(user_dict['settings'])

    @staticmethod
    def court(court_dict:dict, db:dbutils.DBConnection):
        if 'type' in court_dict:
            court_dict['type'] = court_types.get(court_dict['type'], dbconnection=db)._court_type.copy()
        if 'sport_types' in court_dict:
            court_dict['sport_types'] = list(map(lambda x: getters.sport_type(x, db), court_dict['sport_types']))

    @staticmethod
    def game(game_dict:dict, db:dbutils.DBConnection):
        if 'court_id' in game_dict:
            game_dict['court'] = getters.court(game_dict['court_id'], db)
        if 'court_id' in game_dict:
            game_dict['court'] = getters.court(game_dict['court_id'], db)
        if 'game_type' in game_dict:
            game_dict['game_type'] = getters.game_type(game_dict['game_type'], db)
        if 'sport_type' in game_dict:
            game_dict['sport_type'] = getters.court(game_dict['sport_type'], db)
        if 'responsible_user_id' in game_dict:
            user = getters.user(game_dict['responsible_user_id'], db)
            game_dict['responsible_user'] = {'user_id':user['user_id'], 'name':user['first_name']+' '+user['last_name']}
        if 'created_by' in game_dict:
            user = getters.user(game_dict['created_by'], db)
            game_dict['created_by'] = {'user_id':user['user_id'], 'name':user['first_name']+' '+user['last_name']}


@pages.get(['/api/users/get', '/api/users/get/<user_id:int>'])
@handle_error_and_check_auth
def users_get(user_id:int=0):
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else ('user_id' if user_id==0 else '*')
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        if len(fields)==1 and fields[0]=='*' or len(fields)==0 or fields is None:
            fields = dbutils.dbfields['users']
        fields = set(fields)
        fields.difference_update(_available_fields['users_get']['restricted'])
        fields = list(fields)
        users_ = db.execute("SELECT {} FROM users{}".format(
            ', '.join(fields),
            ' WHERE user_id={}'.format(user_id) if user_id!=0 else ''),
                            fields)
        if len(users_)==0:
            raise Error.user_not_found(user_id)
        list(map(strdatetime, users_))
        for user in users_:
            formatters.user(user, db)
        return {'count':len(users_), 'users':users_}


@pages.get('/api/users/current')
@handle_error_and_check_auth
def current_user_get():
    with dbutils.dbopen() as db:
        user = current_user(db, True)._user
        strdatetime(user)
        formatters.user(user, db)
        return dump(user)


@pages.get(['/api/courts/get', '/api/courts/get/<court_id:int>'])
@handle_error_and_check_auth
def courts_get_admin(court_id:int=0):
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else ('court_id' if court_id==0 else '*')
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        if len(fields)==1 and fields[0]=='*' or len(fields)==0 or fields is None:
            fields = dbutils.dbfields['courts']
        fields = set(fields)
        fields.difference_update(_available_fields['courts_get']['restricted'])
        fields = list(fields)
        courts = db.execute("SELECT {} FROM courts{}".format(
            ', '.join(fields),
            ' WHERE court_id={}'.format(court_id) if court_id!=0 else ''),
                            fields)
        if len(courts)==0:
            raise Error.court_not_found(court_id)
        for court in courts:
            formatters.court(court, db)
        return {'count':len(courts), 'courts':courts}


@pages.get(['/api/games/get', '/api/games/get/<game_id:int>'])
@handle_error_and_check_auth
def games_get(game_id:int=0):
    fields = bottle.request.query.get('fields') if 'fields' in bottle.request.query else '*'
    fields = fields.split(',')
    with dbutils.dbopen() as db:
        if len(fields)==1 and fields[0]=='*' or len(fields)==0 or fields is None:
            fields = dbutils.dbfields['games']
        fields = set(fields)
        fields.difference_update(_available_fields['games_get']['restricted'])
        fields = list(fields)
        games = db.execute("SELECT {} FROM games{}".format(
            ', '.join(fields), ' WHERE game_id={}'.format(game_id) if game_id!=0 else ''),
                           fields)
        if len(games)==0:
            raise Error.game_not_found(game_id)
        list(map(strdatetime, games))
        for game in games:
            formatters.game(game, db)
        return {'count':len(games), 'games':games}


@pages.get('/api/games/subscribe/<game_id:int>')
@handle_error_and_check_auth
def subscribe(game_id:int):
    with dbutils.dbopen() as db:
        user = current_user(db, detalized=True)
        game = games.get_by_id(game_id, dbconnection=db)
        if user.banned():
            raise Error.game_conflict(2)
        if 0 < game.capacity() == len(game.subscribed()):
            raise Error.game_conflict(4)
        if user.user_id() in set(game.subscribed()):
            raise Error.game_conflict(5)
        another_game = games.user_game_intersection(user.user_id(), game, dbconnection=db)
        if another_game:
            raise Error.game_conflict(1, another_game.game_id())
        games.subscribe(user.user_id(), game_id, dbconnection=db)
        if game.datetime.tommorow or game.datetime.today:
            user = users.get(user.user_id(), dbconnection=db) if user.user_id()!=pages.auth.current().user_id() else pages.auth.current()
            message = 'На игру "{}" записался {}'.format(create_link.game(game), create_link.user(user))
            utils.spool_func(notificating.site.responsible, game.responsible_user_id(), message, 1, game_id,)
        return {'status':'ok'}


@pages.get('/api/games/unsubscribe/<game_id:int>')
@handle_error_and_check_auth
def unsubscribe(game_id:int):
    with dbutils.dbopen() as db:
        user = current_user(db, detalized=True)
        game = games.get_by_id(game_id, dbconnection=db)
        if user.user_id() not in set(game.subscribed()):
            return pages.PageBuilder("game", game=game, conflict=6)
        if game.datetime.tommorow and game.datetime.time().hour<=12 and datetime.datetime.now().hour>=20:
            return pages.PageBuilder("game", game=game, conflict=11)
        games.unsubscribe(user.user_id(), game_id, dbconnection=db)
        if datetime.datetime.now()-game.datetime()<datetime.timedelta(days=3):
            user = users.get(user.user_id(), dbconnection=db) if user.user_id()!=pages.auth.current().user_id() else pages.auth.current()
            message = '{} отписался от игры "{}"'.format(create_link.user(user), create_link.game(game))
            utils.spool_func(notificating.site.responsible, game.responsible_user_id(), message, 1, game_id)
        return {'status':'ok'}


@pages.get('/api/games/get_subscribed/<game_id:int>')
@handle_error_and_check_auth
def get_subscribed(game_id:int):
    game = games.get_by_id(game_id)
    if not game: raise Error.game_not_found(game_id)
    return {'count': len(game.subscribed()), 'users':[{'user_id':user.user_id(), 'name':str(user.name)} for user in game.subscribed(True)]}


@pages.get('/api/notifications/count')
@handle_error_and_check_auth
def notifications_count():
    with dbutils.dbopen() as db:
        user_id = current_user(db)
        count = notifications.get_count(user_id, dbconnection=db)
        return {'count':count}


@pages.get('/api/notifications/read/<notification_id:int>')
@handle_error_and_check_auth
def read_notification(notification_id:int):
    notifications.read(notification_id)
    return {'status':'ok'}


@pages.get('/api/notifications/delete/<notification_id:int>')
@handle_error_and_check_auth
def delete_notification(notification_id:int):
    notifications.delete(notification_id)
    return {'status':'ok'}


@pages.get('/api/notifications/get')
@handle_error_and_check_auth
def get_notifications():
    with dbutils.dbopen() as db:
        user = current_user(db, True)
        count = notifications.get_count(user.user_id(), dbconnection=db)
        notif = dict()
        notif['all'] = list(map(lambda x: x._notification, notifications.get(user.user_id(), type=0, all=count==0, dbconnection=db)))
        notif['subscribed'] = list(map(lambda x: x._notification, notifications.get(user.user_id(), type=1, all=count==0, dbconnection=db)))
        if user.userlevel.resporgadmin():
            notif['responsible'] = list(map(lambda x: x._notification, notifications.get(user.user_id(), type=2, all=count==0, dbconnection=db)))
        return {'notifications':notif, 'all':count==0}


@pages.get('/api/auth')
@handle_error
@required_param('email', 'password')
def auth():
    email = bottle.request.query.get('email')
    passwd = bottle.request.query.get('password')
    ip = bottle.request.remote_addr
    with dbutils.dbopen() as db:
        db.execute("SELECT user_id FROM users WHERE email='{}' AND passwd='{}'".format(email, passwd))
        if len(db.last())==0:
            raise Error.invalid_auth()
        user_id = db.last()[0][0]
        au = db.execute("SELECT * FROM api_auth WHERE user_id={}".format(user_id))
        token = generate_token()
        while True:
            db.execute("SELECT * FROM api_auth WHERE token='{}'".format(token))
            if len(db.last())>0:
                token = generate_token()
                continue
            if len(au)>0:
                db.execute("UPDATE api_auth SET token='{}', datetime=NOW(), ip='{}' WHERE user_id={} ".format(token, ip, user_id))
            else:
                db.execute("INSERT INTO api_auth VALUES ('{}', '{}', NOW(), {}, '{}')".format(token, email, user_id, ip))
            break
        time.sleep(1.5)
        return {'token':token, 'user_id':user_id}