import datetime

import bottle

import modules
import modules.dbutils
from modules.utils import write_notification, sendmail
import pages
from modules import vk
from models import images, cities, settings


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
        with modules.dbutils.dbopen() as db:
            db.execute("SELECT email FROM users WHERE vkuserid={}".format(data['vkuserid']))
            if len(db.last()) > 0:
                return pages.PageBuilder('auth', error='Вы уже зарегестрированы в системе',
                                         error_description='Используйте пароль, чтобы войти', email=db.last()[0][0])
        data['city'] = user['city']['title'] if 'city' in user else None
        data['first_name'] = user['first_name']
        data['last_name'] = user['last_name']
        data['phone'] = user['mobile_phone'] if 'mobile_phone' in user else None
        data['sex'] = 'male' if user['sex'] == 2 else ('female' if user['sex'] == 1 else None)
        data['email'] = email if email else None
        data['bdate'] = vk.convert_date(user['bdate']) if 'bdate' in user else None
        for city in cities_list:
            if city['title'] == data['city']:
                data['city_id'] = city['city_id']
                break

        data['vkphoto'] = user['photo_max']

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
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}

        params['regdate'] = str(datetime.date.today())
        params['lasttime'] = str(datetime.datetime.now())
        params.pop('confirm_passwd')
        params['phone'] = params['phone'] if params['phone'] else 'Не указан'

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
                params['city_id'] = 1
            db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']))
            if len(db.last()) > 0:
                params.pop('email')
                return pages.PageBuilder('registration', error='Ошибка',
                                         error_description='Пользователь с таким email уже зарегестрирован',
                                         cities=cities, **params)
            params['settings'] = settings.default().format()
            sql = 'INSERT INTO users ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
            db.execute(sql)
            db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']))
            user_id = db.last()[0][0]
            # pages.auth_dispatcher.login(params['email'], params['passwd'])
            if 'avatar' in bottle.request.files:
                images.save_avatar(user_id, bottle.request.files.get('avatar'))
            token = modules.generate_token()
            sendmail(
                'Чтобы активировать профиль, перейдите по ссылке http://sportcourts.ru/activate?token={}'.format(
                    token), params['email'], 'Активация профиля')
            db.execute("INSERT INTO activation (user_id, token) VALUES ({}, '{}')".format(user_id, token))
            write_notification(user_id, "Проверьте свою почту чтобы активировать профиль!", 1)
            return pages.PageBuilder('text', message='Проверьте почту',
                                     description='Вам было отправлено письмо с инструкцией по активации профиля')

    get.route = '/registration'
    post.route = get.route