import os
import urllib.request
import datetime

from PIL import Image
import bottle

import modules
import modules.dbutils
import pages
from modules import vk, sendmail


class Registration(pages.Page):
    path = ['register', 'registration']

    def get_code(self, cities):
        code = bottle.request.query.code
        url = "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri=http://{3}:{4}/registration"
        url = url.format(modules.config['api']['vk']['appid'],
                         modules.config['api']['vk']['secret'], code,
                         modules.config['server']['ip'], modules.config['server']['port'])
        response = urllib.request.urlopen(url)
        response = response.read().decode()
        response = bottle.json_loads(response)
        if 'error' in response:
            return pages.Template('registration', error=response['error'],
                                  error_description=response['error_description'], cities=cities)
        access_token, user_id, email = response['access_token'], response['user_id'], response.get('email')
        user = vk.exec(access_token, 'users.get', fields=['sex', 'bdate', 'city', 'photo_max', 'contacts'])[0]
        data = dict()
        data['vkuserid'] = user_id
        with modules.dbutils.dbopen() as db:
            db.execute("SELECT email FROM users WHERE vkuserid={}".format(data['vkuserid']))
            if len(db.last()) > 0:
                return pages.Template('auth',
                                      error='Вы уже зарегестрированы в системе',
                                      error_description='Используйте пароль, чтобы войти',
                                      email=db.last()[0][0])
        data['city'] = user['city']['title'] if 'city' in user else None
        data['first_name'] = user['first_name']
        data['last_name'] = user['last_name']
        data['phone'] = user['mobile_phone'] if 'mobile_phone' in user else None
        data['sex'] = 'male' if user['sex'] == 2 else ('female' if user['sex'] == 1 else None)
        data['email'] = email if email else None
        data['bdate'] = vk.convert_date(user['bdate']) if 'bdate' in user else None
        for city in cities:
            if city['title'] == data['city']:
                data['city_id'] = city['city_id']
                break
        fullname = '/bsp/data/avatars/temp{}.jpg'.format(user['id'])
        urllib.request.urlretrieve(user['photo_max'], fullname)
        Image.open(fullname).crop().resize((200, 200)).save(fullname)
        data['photo'] = 'http://sportcourts.ru/avatars/temp{}'.format(user['id'])
        data = {i: data[i] for i in data if data[i]}
        return pages.Template('registration', cities=cities, **data)

    @pages.handleerrors('registration')
    def get(self):
        if pages.loggedin():
            return bottle.redirect('/profile')
        with modules.dbutils.dbopen() as db:
            cities = db.execute("SELECT city_id, title FROM cities", ['city_id', 'title'])
        if 'code' in bottle.request.query:
            return self.get_code(cities)
        else:
            return pages.Template('registration', cities=cities)

    def post(self):
        params = {i: bottle.request.forms[i] for i in bottle.request.forms}
        params.pop("submit_order")
        params.pop("confirm_passwd")
        params['regdate'] = str(datetime.date.today())
        params['lasttime'] = params['regdate']

        params['first_name'] = bottle.request.forms.get('first_name')
        params['middle_name'] = bottle.request.forms.get('middle_name')
        params['last_name'] = bottle.request.forms.get('last_name')
        params['city'] = bottle.request.forms.get('city')
        city_title = params['city']
        params.pop('city')

        vkavatar = ''
        if 'vkavatar' in bottle.request.forms:
            params.pop('vkavatar')
            vkavatar = bottle.request.forms.get('vkavatar')

        with modules.dbutils.dbopen() as db:
            cities = db.execute("SELECT city_id, title FROM cities", ['city_id', 'title'])
            db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
            if len(db.last()) > 0:
                params['city_id'] = db.last()[0][0]
            else:
                params['city_id'] = 1
            db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']))
            if len(db.last()) > 0:
                return pages.Template('registration', error='Ошибка',
                                      error_description='Пользователь с таким email уже зарегестрирован',
                                      cities=cities)
            sql = 'INSERT INTO users ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
            db.execute(sql)
            db.execute('SELECT user_id, admin, user_type FROM users WHERE email="{}"'.format(params['email']),
                       ['user_id', 'admin', 'user_type'])
            user_id = db.last()[0]['user_id']
            bottle.response.set_cookie('user_id', user_id, modules.config['secret'])
            bottle.response.set_cookie('adminlevel', db.last()[0]['admin'], modules.config['secret'])
            bottle.response.set_cookie('activated', 0, modules.config['secret'])
            bottle.response.set_cookie('user_type', db.last()[0]['user_type'], modules.config['secret'])
            db.execute("UPDATE users SET lasttime=NOW() WHERE user_id={}".format(user_id))
            if vkavatar:
                os.rename("/bsp/data/avatars/{}.jpg".format(os.path.split(vkavatar)[-1]),
                          "/bsp/data/avatars/{}.jpg".format(user_id))
            elif 'avatar' in bottle.request.files:
                filename = str(user_id) + '.jpg'
                dirname = '/bsp/data/avatars'
                fullname = os.path.join(dirname, filename)
                if os.path.exists(fullname):
                    os.remove(fullname)
                bottle.request.files.get('avatar').save(fullname)
                im = Image.open(fullname)
                im.crop().resize((200, 200)).save(fullname)
                im.close()
            token = modules.generate_token()
            sendmail(
                'Чтобы активировать профиль, перейдите по ссылке http://sportcourts.ru/activate?token={}'.format(
                    token), params['email'])
            db.execute("INSERT INTO activation (user_id, token) VALUES ({}, '{}')".format(user_id, token))
            pages.write_notification(user_id, "Проверьте свою почту чтобы активировать профиль!", 1)
            return bottle.redirect('/profile')