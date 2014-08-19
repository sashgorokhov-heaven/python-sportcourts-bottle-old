import urllib.request
import datetime

import bottle

import modules
import modules.dbutils
import pages
from modules import vk


class Registration(pages.Page):
    path = ['reg', 'register', 'registration']

    def execute(self, method:str):
        if method == 'GET': return self.get().template()
        if method == 'POST':
            data = self.post()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    @pages.setlogin
    @pages.handleerrors('registration')
    def get(self):
        if 'code' in bottle.request.query:
            code = bottle.request.query.code
            url = "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri=http://{3}:{4}/registration"
            url = url.format(modules.config['api']['vk']['appid'],
                             modules.config['api']['vk']['secret'],
                             code,
                             modules.config['server']['ip'],
                             modules.config['server']['port']
            )
            response = urllib.request.urlopen(url)
            response = response.read().decode()
            response = bottle.json_loads(response)
            if 'error' in response:
                return pages.Template('registration', error=response['error'],
                                      error_description=response['error_description'])
            access_token, user_id, email = response['access_token'], response['user_id'], response.get('email')
            user = vk.exec(access_token, 'users.get', fields=['sex', 'bdate', 'city'])[0]
            data = dict()
            data['city'] = user['city']['title'] if 'city' in user else None
            data['first_name'] = user['first_name']
            data['last_name'] = user['last_name']
            data['sex'] = 'male' if user['sex'] == 2 else ('female' if user['sex'] == 1 else None)
            data['email'] = email if email else None
            data['bdate'] = vk.convert_date(user['bdate']) if 'bdate' in user else None
            data = {i: data[i] for i in data if data[i]}
            return pages.Template('registration', **data)
        else:
            return pages.Template('registration')

    @pages.handleerrors('registration')
    def post(self):
        params = {i: bottle.request.forms[i] for i in bottle.request.forms}
        params.pop("submit_order")
        params.pop("confirm_passwd")
        params['regdate'] = str(datetime.date.today())
        params['lasttime'] = params['regdate']

        params['first_name'] = bottle.request.forms.getunicode('first_name')
        params['middle_name'] = bottle.request.forms.getunicode('middle_name')
        params['last_name'] = bottle.request.forms.getunicode('last_name')

        # print(params)

        with modules.dbutils.dbopen() as db:
            db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']))
            if len(db.last()) > 0:
                return pages.Template('registration', error='Ошибка',
                                      error_description='Такой пользователь уже существует',
                                      login=True)
            sql = 'INSERT INTO users ({dbkeylist}) VALUES ({dbvaluelist})'
            keylist = list(params.keys())
            sql = sql.format(
                dbkeylist=', '.join(keylist),
                dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
            db.execute(sql)
            # db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']), ['user_id'])
        return bottle.redirect('/')