import datetime
import json
import pickle

import bottle
import modules
import modules.dbutils
import pages
from modules import vk
from models import images, cities, settings, notifications, mailing, activation, users
import modules.logging

class Registration(pages.Page):
    def get_code(self, cities_list):
        code = bottle.request.query.code
        try:
            access_token, user_id, email = vk.auth_code(code, '/registration')
        except ValueError as e:
            return pages.PageBuilder('registration', cities=cities_list, error=e.vkerror['error'],
                                     error_description=e.vkerror['error_description'])

        user = vk.exec(access_token, 'users.get', fields=['sex', 'bdate', 'city', 'photo_max', 'contacts'])[0]

        data = dict()
        data['vkuserid'] = user_id
        pickledata = {'vkuserid': user_id}
        with modules.dbutils.dbopen() as db:
            db.execute("SELECT email FROM users WHERE vkuserid={}".format(data['vkuserid']))
            if len(db.last()) > 0:
                return pages.PageBuilder('auth', error='Вы уже зарегестрированы в системе',
                                         error_description='Используйте пароль, чтобы войти', email=db.last()[0][0])
        data['city'] = user['city']['title'] if 'city' in user else None
        data['first_name'] = user['first_name']
        data['last_name'] = user['last_name']
        data['sex'] = 'male' if user['sex'] == 2 else ('female' if user['sex'] == 1 else None)
        data['email'] = email if email else None
        try:  # dirty hack
            data['bdate'] = vk.convert_date(user['bdate']) if 'bdate' in user else None
        except:
            pass
        for city in cities_list:
            if city['title'] == data['city']:
                data['city_id'] = city['city_id']
                break

        if user['photo_max'].find('camera') == -1:
            pickledata['vkphoto'] = user['photo_max']
            data['vkphoto'] = user['photo_max']

        bottle.response.set_cookie('vkinfo', pickle.dumps(pickledata), modules.config['secret'])

        data = {i: data[i] for i in data if data[i]}
        return pages.PageBuilder('registration', cities=cities_list, **data)

    def get(self):
        if pages.auth_dispatcher.loggedin():
            raise bottle.redirect('/profile')
        cities_list = cities.get(0)
        if 'code' in bottle.request.query:
            return self.get_code(cities_list)
        else:
            return pages.PageBuilder('registration', cities=cities_list)

    def post(self):
        if pages.auth_dispatcher.loggedin():
            raise bottle.redirect('/profile')
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}

        if params['bdate'] == '00.00.0000':
            # TODO: проверить формат
            with modules.dbutils.dbopen() as db:
                cities = db.execute("SELECT city_id, title FROM cities", ['city_id', 'title'])
            return pages.PageBuilder('registration', error='Ошибка',
                                     error_description='Неверно указана дата рождения',
                                     cities=cities, **params)

        params['regdate'] = str(datetime.date.today())
        params['lasttime'] = str(datetime.datetime.now())
        params.pop('confirm_passwd')
        params['phone'] = params['phone'] if params['phone'] else 'Не указан'

        params['bdate'] = params['bdate'].split('.')
        params['bdate'].reverse()
        params['bdate'] = '-'.join(params['bdate'])

        city_title = params['city']
        params.pop('city')

        if 'avatar' in bottle.request.forms:
            params.pop('avatar')

        with modules.dbutils.dbopen() as db:
            cities = db.execute("SELECT city_id, title FROM cities", ['city_id', 'title'])
            db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
            if len(db.last()) > 0:
                params['city_id'] = db.last()[0][0]
            else:
                params['bdate'] = params['bdate'].split('-')
                params['bdate'].reverse()
                params['bdate'] = '.'.join(params['bdate'])
                return pages.PageBuilder('registration', error='Ошибка',
                                         error_description='Мы не работаем в городе {}'.format(city_title),
                                         cities=cities, **params)
            db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']))
            if len(db.last()) > 0:
                params.pop('email')
                params['bdate'] = params['bdate'].split('-')
                params['bdate'].reverse()
                params['bdate'] = '.'.join(params['bdate'])
                return pages.PageBuilder('registration', error='Ошибка',
                                         error_description='Пользователь с таким email уже зарегестрирован',
                                         cities=cities, **params)
            if datetime.date(*list(map(int, params['bdate'].split('-')))) > datetime.date.today():
                params['bdate'] = params['bdate'].split('-')
                params['bdate'].reverse()
                params['bdate'] = '.'.join(params['bdate'])
                return pages.PageBuilder('registration', error='Ошибка',
                                         error_description='Ты из будущего?',
                                         cities=cities, **params)
            if datetime.date.today() - datetime.date(*list(map(int, params['bdate'].split('-')))) < datetime.timedelta(
                    days=2555):
                params['bdate'] = params['bdate'].split('-')
                params['bdate'].reverse()
                params['bdate'] = '.'.join(params['bdate'])
                return pages.PageBuilder('registration', error='Ошибка',
                                         error_description='Такой маленький, а уже пользуешься интернетом?',
                                         cities=cities, **params)
            params['settings'] = settings.default().format()
            vkparams = bottle.request.get_cookie('vkinfo', '', modules.config['secret'])
            if vkparams:
                vkparams = pickle.loads(vkparams)
                params['vkuserid'] = vkparams['vkuserid']

            sql = 'INSERT INTO users ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
            db.execute(sql)
            db.execute(
                'SELECT user_id, vkuserid, first_name, last_name FROM users WHERE email="{}"'.format(params['email']))
            user_id = db.last()[0][0]
            vkuserid = db.last()[0][1]
            username = db.last()[0][2] + ' ' + db.last()[0][3]
            # pages.auth_dispatcher.login(params['email'], params['passwd'])
            if 'avatar' in bottle.request.files:
                images.save_avatar(user_id, bottle.request.files.get('avatar'))
            elif vkparams and 'vkphoto' in vkparams:
                images.save_avatar_from_url(user_id, vkparams['vkphoto'])
            token = activation.create(user_id, dbconnection=db)
            mailing.send_to_user(user_id,
                                 'Чтобы активировать профиль, перейдите по ссылке http://sportcourts.ru/activate?token={}'.format(
                                     token),
                                 'Активация профиля',
                                 True,
                                 dbconnection=db)
            notifications.add(user_id, "Проверьте свою почту чтобы активировать профиль!", 1, dbconnection=db)
            if vkuserid:
                friends = vk.exec(None, "friends.get", user_id=vkuserid)['items']
                if len(friends) > 0:
                    friends = map(str, friends)
                    db.execute("SELECT user_id, first_name, last_name FROM users WHERE vkuserid IN ({})".format(
                        ','.join(friends)))
                    for friend in db.last():
                        friend_id = friend[0]
                        friend_name = friend[1] + ' ' + friend[2]
                        try:
                            notifications.add(friend_id,
                                              'Ваш друг <a href="/profile?user_id={}">{}</a> зарегистрировался на сайте!'.format(
                                                  user_id, username))
                            notifications.add(user_id,
                                              'Ваш друг <a href="/profile?user_id={}">{}</a> уже зарегистрирован на сайте.'.format(
                                                  friend_id, friend_name))
                        except:
                            notifications.add(friend_id,
                                              'Ваш <a href="/profile?user_id={}">друг</a> зарегистрировался на сайте!'.format(
                                                  user_id))
                            notifications.add(user_id,
                                              'Ваш <a href="/profile?user_id={}">друг</a> уже зарегистрирован на сайте.'.format(
                                                  friend_id))
                        users.add_friend(user_id, friend_id, dbconnection=db)
                        users.add_friend(friend_id, user_id, dbconnection=db)
            return pages.PageBuilder('text', message='Проверьте почту',
                                     description='Вам было отправлено письмо с инструкцией по активации профиля')

    get.route = '/registration'
    post.route = get.route