import urllib.request
import datetime

import modules.vk as vk


__author__ = 'sashgorokhov'

import bottle, os, json

config = json.load(open(os.path.join('modules', 'config.json'), 'r'))

SERVER_ROOT = config['server_root']
bottle.TEMPLATE_PATH.append('views')

bottle.debug(config['debug'])


@bottle.error(404)
def error404(error):
    return bottle.template('404')


@bottle.route('/')
@bottle.route('/main')
def index():
    return bottle.template('index')


@bottle.get('/registration')
def registration():
    if 'code' in bottle.request.query:
        code = bottle.request.query.code
        url = "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri=http://{3}:{4}/registration"
        url = url.format(config['api']['vk']['appid'],
                         config['api']['vk']['secret'],
                         code,
                         config['server']['ip'],
                         config['server']['port']
        )
        response = urllib.request.urlopen(url)
        response = response.read().decode()
        response = bottle.json_loads(response)

        if 'error' in response:
            return bottle.template('registration', error=response['error'],
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
        return bottle.template('registration', **data)
    else:
        return bottle.template('registration')


@bottle.post('/registration')
def register():
    params = {i: bottle.request.forms[i] for i in bottle.request.forms}
    params.pop("submit_order")
    params.pop("confirm_passwd")
    params['regdate'] = str(datetime.date.today())
    params['lasttime'] = params['regdate']
    import modules.dbutils

    with modules.dbutils.dbopen() as db:
        db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']))
        if len(db.last()) > 0:
            return bottle.template('registration', error='Ошибка',
                                   error_description='Такой пользователь уже существует')
        sql = 'INSERT INTO users ({dbkeylist}) VALUES ({dbvaluelist})'
        keylist = list(params.keys())
        sql = sql.format(
            dbkeylist=', '.join(keylist),
            dbvaluelist=', '.join(["'{}'".format(str(params[key])) for key in keylist]))
        db.execute(sql)
        db.execute('SELECT user_id FROM users WHERE email="{}"'.format(params['email']), ['user_id'])
    return bottle.redirect('/')


@bottle.route('/<path:path>')
def static_route(path):
    return bottle.static_file(path, os.path.join(SERVER_ROOT, 'static'))


application = bottle.default_app()

