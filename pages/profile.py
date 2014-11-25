import bottle
import json
from modules import vk

import pages
import dbutils
from models import users, cities, images, games, ampluas


@pages.get('/profile/<user_id:int>')
def get_by_id(user_id:int):
    with dbutils.dbopen() as db:
        if user_id == pages.auth.current().user_id():
            raise bottle.redirect('/profile')
        user = users.get(user_id, dbconnection=db)
        if len(user) == 0:
            raise bottle.HTTPError(404)
        page = pages.PageBuilder('profile', user=user,
                                 myfriend=users.are_friends(
                                     pages.auth.current().user_id(),
                                     user_id, dbconnection=db))
        page.add_param('user_games',
                       games.get_by_id(games.get_user_played_games(user_id, dbconnection=db), dbconnection=db))
        page.add_param('responsible_games',
                       games.get_by_id(games.get_responsible_games(user_id, dbconnection=db), dbconnection=db))
        page.add_param('organizer_games', games.get_all(dbconnection=db))
        with dbutils.dbopen(**dbutils.logsdb_connection) as logsdb:
            logsdb.execute("SELECT COUNT(DISTINCT(ip)), COUNT(ip) FROM access WHERE (path='/profile?user_id={}' or path='/profile/{}') and user_id!=0".format(user_id, user_id))
            page.add_param('views', logsdb.last()[0][1])
            page.add_param('uviews', logsdb.last()[0][0])
        return page


@pages.get('/profile/edit')
@pages.only_loggedin
def edit():
    with dbutils.dbopen() as db:
        _cities = cities.get(0, dbconnection=db)
        user = users.get(pages.auth.current().user_id(), dbconnection=db)
        _ampluas = ampluas.get(0, dbconnection=db)
        _ampluas = {
            sport_type_title: list(filter(lambda x: x.sport_type(True).title() == sport_type_title, _ampluas)) for
            sport_type_title in {i.sport_type(True).title() for i in _ampluas}}
        return pages.PageBuilder('editprofile', user=user, cities=_cities, ampluas=_ampluas,
                                 haveavatar=images.have_avatar(pages.auth.current().user_id()))


@pages.post('/profile/edit')
@pages.only_loggedin
def edit_post():
    params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
    city_title = params['city']
    params.pop('city')
    if 'ampluas[]' in params:
        params.pop('ampluas[]')
        params['ampluas'] = bottle.request.forms.getall('ampluas[]')
        params['ampluas'] = '|' + '|'.join(params['ampluas']) + '|'
    else:
        params['ampluas'] = ''
    if 'avatar' in params:
        if isinstance(params['avatar'], str):
            images.delete_avatar(pages.auth.current().user_id())
        params.pop('avatar')
    elif 'avatar' in bottle.request.files:
        images.save_avatar(pages.auth.current().user_id(), bottle.request.files.get('avatar'))
    with dbutils.dbopen() as db:
        db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
        if len(db.last()) > 0:
            params['city_id'] = db.last()[0][0]
        else:
            params['city_id'] = 1
        sql = "UPDATE users SET {} WHERE user_id={}".format(
            ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
            pages.auth.current().user_id())
        db.execute(sql)
        raise bottle.redirect('/profile')


@pages.get('/profile')
@pages.only_loggedin
def get():
    with dbutils.dbopen() as db:
        user_id = pages.auth.current().user_id()
        user = users.get(user_id, dbconnection=db)
        page = pages.PageBuilder('profile', user=user)
        page.add_param('user_games',
                       games.get_by_id(games.get_user_played_games(user_id, dbconnection=db), dbconnection=db))
        page.add_param('responsible_games',
                       games.get_by_id(games.get_responsible_games(user_id, dbconnection=db), dbconnection=db))
        page.add_param('organizer_games',
                       games.get_by_id(games.get_organizer_games(user_id, dbconnection=db), dbconnection=db))
        with dbutils.dbopen(**dbutils.logsdb_connection) as logsdb:
            logsdb.execute("SELECT COUNT(DISTINCT(ip)), COUNT(ip) FROM access WHERE path='/profile?user_id={}' and user_id!=0".format(user_id))
            page.add_param('views', logsdb.last()[0][1])
            page.add_param('uviews', logsdb.last()[0][0])
        return page


@pages.get('/profile/settings')
@pages.only_loggedin
def settings():
    return pages.PageBuilder("settings")

@pages.post('/profile/settings')
@pages.only_loggedin
def settings_post():
    with dbutils.dbopen() as db:
        send_email = 'email_notify' in bottle.request.forms
        show_phone = bottle.request.forms['phone']
        db.execute("UPDATE users SET settings='{}' WHERE user_id={}".format(
            json.dumps({'send_mail': send_email, 'show_phone': show_phone}), pages.auth.current().user_id()))
        user = users.get(pages.auth.current().user_id(), dbconnection=db)
        pages.auth.reloaduser(user._pure)
        raise bottle.redirect("/profile")


@pages.get('/profile/addfriend/<user_id:int>')
@pages.only_loggedin
def addfriend(user_id:int):
    users.add_friend(pages.auth.current().user_id(), user_id)


@pages.get('/profile/removefriend/<user_id:int>')
@pages.only_loggedin
def addfriend(user_id:int):
    users.remove_friend(pages.auth.current().user_id(), user_id)


@pages.get('/profile/setvkid')
@pages.only_loggedin
def setvkid():
    if 'code' not in bottle.request.query:
        raise bottle.HTTPError(404)
    code = bottle.request.query.get('code')
    try:
        access_token, user_id, email = vk.auth_code(code, '/setvkid')
    except ValueError as e:
        return pages.templates.message(error=e.vkerror['error'], error_description=e.vkerror['error_description'])
    users.setvkuserid(pages.auth.current().user_id(), int(user_id))
    raise bottle.redirect('/profile')