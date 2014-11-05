import datetime
import json
import pickle

import bottle
import config

import dbutils
import pages
from modules import vk
from models import images, cities, notifications, mailing, activation, users

class Registration(pages.Page):
    def get(self):
        if pages.auth.loggedin():
            raise bottle.redirect('/profile')
        if 'ref' in bottle.request.query:
            referer = bottle.request.query.get('ref')
            with dbutils.dbopen() as db:
                db.execute("SELECT user_id, first_name, last_name FROM users WHERE user_id='{}'".format(referer))
                if len(db.last())==0:
                    return pages.templates.message('Ошибка', 'Неверный реферальный код <b>{}</b>'.format(referer))
                pages.set_cookie('referer', referer)
                raise bottle.redirect('/')

        if 'code' in bottle.request.query:
            code = bottle.request.query.get('code')
            _cities = cities.get(0)
            try:
                access_token, user_id, email = vk.auth_code(code, '/registration')
            except ValueError as e:
                return pages.PageBuilder('registration', cities=_cities, error=e.vkerror['error'],
                                         error_description=e.vkerror['error_description'])
            user = vk.exec(access_token, 'users.get', fields=['sex', 'bdate', 'city', 'photo_max', 'contacts'])[0]
            data = dict()
            data['vkuserid'] = user_id
            pickledata = {'vkuserid': user_id}
            data['first_name'] = user['first_name']
            data['last_name'] = user['last_name']
            data['sex'] = 'male' if user['sex'] == 2 else ('female' if user['sex'] == 1 else None)
            try:  # dirty hack
                data['bdate'] = vk.convert_date(user['bdate']) if 'bdate' in user else None
            except:
                pass

            if 'camera' not in user['photo_max']:
                pickledata['vkphoto'] = user['photo_max']
                data['vkphoto'] = user['photo_max']

            pages.set_cookie('vkinfo', pickle.dumps(pickledata))
            token = pages.get_cookie('token', None)
            if not token:
                return pages.PageBuilder('registration', cities=_cities, error='Не найден код.', **data)
            data['token'] = token
            data['email'] = activation.get(token)
            data = {i: data[i] for i in data if data[i]}
            return pages.PageBuilder('registration', cities=_cities, **data)

        if 'token' in bottle.request.query:
            token = bottle.request.query.get('token')
            with dbutils.dbopen() as db:
                try:
                    email = activation.get(token, dbconnection=db)
                except ValueError:
                    return pages.templates.message('Ошибка', 'Неверный код.')
                pages.set_cookie('token', token)
                status = activation.status(email, dbconnection=db)
                if status==0:
                    activation.activate(email, dbconnection=db)
                elif status==2:
                    return pages.PageBuilder('auth',
                                             error='Вы уже зарегестрированы в системе',
                                             error_description='Используйте пароль, чтобы войти', email=email)
                _cities = cities.get(0, dbconnection=db)
                return pages.PageBuilder('registration', cities=_cities, email=email, token=token)
        raise bottle.HTTPError(404)

    def post_email(self):
        email = bottle.request.forms.get('email')
        with dbutils.dbopen() as db:
            db.execute("SELECT user_id, first_name, last_name FROM users WHERE email='{}'".format(email))
            if len(db.last())>0: # уже зареган
                return json.dumps({'error_code':1, 'error_data':db.last()[0]})
            try:
                token = activation.create(email, dbconnection=db)
            except ValueError as e: # юзер активирован
                return json.dumps({'error_code':2, 'error_data':[list(e.args)[1:]]})
            except KeyError as e: # юзер зареган
                return json.dumps({'error_code':3, 'error_data':[list(e.args)[1:]]})
            mailing.sendhtml(
                pages.PageBuilder('mail_activation', token=token).template(),
                email,
                'Чтобы подтвердить email, перейдите по ссылке http://{}/registration?token={}'.format(config.server, token),
                'Подтверждение email')
            return json.dumps({'error_code':0})

    def post_reg(self):
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        _cities = cities.get(0)
        token = bottle.request.forms.get('token')
        params['email'] = activation.get(token)
        params.pop('token')
        params['token'] = token

        if params['bdate'] == '00.00.0000':
            return pages.PageBuilder('registration', error='Ошибка',
                                     error_description='Неверно указана дата рождения',
                                     cities=_cities, **params)

        params['regdate'] = str(datetime.date.today())
        params['lasttime'] = str(datetime.datetime.now())

        params.pop('confirm_passwd')

        city_title = 'Екатеринбург' # TODO
        #params.pop('city')

        if 'avatar' in bottle.request.forms:
            params.pop('avatar')

        with dbutils.dbopen() as db:
            db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
            if len(db.last()) > 0:
                params['city_id'] = db.last()[0][0]
            else:
                return pages.PageBuilder('registration', error='Ошибка',
                                         error_description='Мы не работаем в городе {}'.format(city_title),
                                         cities=_cities, **params)
            try:
                date = params['bdate'].split('.')
                date.reverse()
                date = datetime.date(*list(map(int, date)))
                if date > datetime.date.today():
                    params.pop('bdate')
                    return pages.PageBuilder('registration', error='Ошибка',
                                             error_description='Ты из будущего?',
                                             cities=_cities, **params)
                if datetime.date.today() - date < datetime.timedelta(
                        days=2555):
                    params.pop('bdate')
                    return pages.PageBuilder('registration', error='Ошибка',
                                             error_description='Такой маленький, а уже пользуешься интернетом?',
                                             cities=_cities, **params)
                params['bdate'] = params['bdate'].split('.')
                params['bdate'].reverse()
                params['bdate'] = '-'.join(params['bdate'])
            except:
                params.pop('bdate')
                return pages.PageBuilder('registration', error='Ошибка',
                                             error_description='Ошибка преобразования даты рождения.',
                                             cities=_cities, **params)
            vkparams = pages.get_cookie('vkinfo', '')
            bottle.response.delete_cookie('vkinfo')
            if vkparams:
                vkparams = pickle.loads(vkparams)
                params['vkuserid'] = vkparams['vkuserid']

            referer = pages.get_cookie('referer', 0)
            if referer:
                params['referer'] = referer
            params.pop('token')
            sql = 'INSERT INTO users ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
            db.execute(sql)
            db.execute(
                "SELECT user_id, vkuserid, first_name, last_name, email, passwd FROM users WHERE email='{}'".format(params['email']))
            user_id = db.last()[0][0]
            email = db.last()[0][4]
            passwd = db.last()[0][5]
            vkuserid = db.last()[0][1]
            first_name = db.last()[0][2]
            username = db.last()[0][2] + ' ' + db.last()[0][3]
            if 'avatar' in bottle.request.files:
                images.save_avatar(user_id, bottle.request.files.get('avatar'))
            elif vkparams and 'vkphoto' in vkparams:
                images.save_avatar_from_url(user_id, vkparams['vkphoto'])
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
            activation.register(params['email'], dbconnection=db)
            pages.delete_cookie('referer')
            pages.delete_cookie('token')
            pages.auth.login(email, passwd)
            raise bottle.redirect('/profile')

    def post(self, action):
        if pages.auth.loggedin(): raise bottle.redirect('/profile')
        if action=='email':
            return self.post_email()
        if action=='reg':
            return self.post_reg()
        raise bottle.HTTPError(404)

    get.route = '/registration'
    post.route = '/registration/<action>'
