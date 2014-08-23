import os
import datetime

from PIL import Image
import bottle

import pages
import modules
import modules.dbutils


months = ['Января', 'Февраля',
          'Марта', 'Апреля',
          'Мая', 'Июня', 'Июля',
          'Августа', 'Сентября',
          'Октября', 'Ноября', 'Декабря']
days = ['Понедельник', 'Вторник', 'Среда',
        'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def beautifuldate(datetime:str):
    date, day = datetime.split(' ')[0].split('-')[1:]
    return '{} {}'.format(day, months[int(date) - 1])


def beautifultime(datetime:str):
    return ':'.join(datetime.split(' ')[-1].split(':')[:-1])


class Profile(pages.Page):
    path = ['profile']

    @pages.setlogin
    def get(self):
        if 'user_id' in bottle.request.query:
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(bottle.request.query.user_id)
                if len(user) == 0:
                    raise bottle.HTTPError(404)
                user = user[0]
                modules.dbutils.strdates(user)
                user['bdate'] = str(round((datetime.date.today() - datetime.date(
                    *list(map(int, user['bdate'].split('-'))))).total_seconds() // 31556926)) + ' лет'
                user['lasttime'] = '{} в {}'.format(beautifuldate(user['lasttime']), beautifultime(user['lasttime']))
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('profile', user=user)
        elif 'edit' in bottle.request.query and pages.loggedin():
            with modules.dbutils.dbopen() as db:
                cities = db.execute("SELECT city_id, title FROM cities", ['city_id', 'title'])
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                modules.dbutils.strdates(user)
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('editprofile', user=user, cities=cities)
        elif pages.loggedin():
            with modules.dbutils.dbopen() as db:
                user = modules.dbutils.get(db).user(pages.getuserid())[0]
                modules.dbutils.strdates(user)
                user['bdate'] = str(round((datetime.date.today() - datetime.date(
                    *list(map(int, user['bdate'].split('-'))))).total_seconds() // 31556926)) + ' лет'
                user['lasttime'] = '{} в {}'.format(beautifuldate(user['lasttime']), beautifultime(user['lasttime']))
                user['city'] = modules.dbutils.get(db).city(user['city_id'])[0]
                user.pop('city_id')
                return pages.Template('profile', user=user)
        raise bottle.HTTPError(404)

    @pages.setlogin
    def post(self):
        if not pages.loggedin():
            raise bottle.HTTPError(404)
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        params.pop("submit_profile")

        params['first_name'] = bottle.request.forms.get('first_name')
        params['middle_name'] = bottle.request.forms.get('middle_name')
        params['last_name'] = bottle.request.forms.get('last_name')
        params['city'] = bottle.request.forms.get('city')
        city_title = params['city']
        params.pop('city')

        if 'avatar' in params:
            params.pop('avatar')

        if 'avatar' in bottle.request.files:
            filename = str(pages.getuserid()) + '.jpg'
            dirname = '/bsp/data/avatars'
            fullname = os.path.join(dirname, filename)
            if os.path.exists(fullname):
                os.remove(fullname)
            bottle.request.files.get('avatar').save(fullname)
            im = Image.open(fullname)
            im.crop().resize((200, 200)).save(fullname)
            im.close()

        with modules.dbutils.dbopen() as db:
            db.execute("SELECT city_id FROM cities WHERE title='{}'".format(city_title))
            if len(db.last()) > 0:
                params['city_id'] = db.last()[0][0]
            else:
                params['city_id'] = 1
            sql = "UPDATE users SET {} WHERE user_id={}".format(
                ', '.join(['{}="{}"'.format(i, params[i]) for i in params]),
                pages.getuserid())
            db.execute(sql)
            bottle.redirect('/profile')
