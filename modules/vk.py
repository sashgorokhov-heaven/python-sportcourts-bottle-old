import json
import urllib.request
import urllib.parse

import bottle

import modules


def exec(token:str, method:str, **kwargs) -> dict:
    params = list()
    for key in kwargs:
        if len(str(kwargs[key])) != 0:
            if isinstance(kwargs[key], list):
                params.append((key, ','.join(map(str, kwargs[key]))))
            else:
                params.append((key, str(kwargs[key])))
    params.append(("access_token", token))
    params.append(('v', '5.24'))
    url = 'https://api.vk.com/method/{0}?{1}'.format(method, urllib.parse.urlencode(params))
    response = urllib.request.urlopen(url).read().decode()
    response = json.loads(response)
    return response['response']


def auth_code(code:str, redirec_page:str) -> (str, int, str):
    url = "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri=http://{3}:{4}/auth"
    url = url.format(modules.config['api']['vk']['appid'],
                     modules.config['api']['vk']['secret'], code,
                     modules.config['server']['ip'], modules.config['server']['port'])
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        e = ValueError()
        e.vkerror = dict()
        e.vkerror['error'] = "Auth error"
        e.vkerror['error_description'] = "Unauthorized"
        raise e
    response = response.read().decode()
    response = bottle.json_loads(response)
    if 'error' in response:
        e = ValueError()
        e.vkerror = response
        raise e
    return response['access_token'], response['user_id'], response.get('email')


def convert_date(vkdate:str) -> str:
    vkdate = vkdate.split('.')
    vkdate.reverse()
    vkdate[1] = vkdate[1] if len(vkdate[1]) == 2 else '0' + vkdate[1]
    vkdate[2] = vkdate[2] if len(vkdate[2]) == 2 else '0' + vkdate[2]
    return '-'.join(vkdate)