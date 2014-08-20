import json
import urllib.request
import urllib.parse


def exec(token:str, method:str, **kwargs):
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


def convert_date(vkdate:str):
    vkdate = vkdate.split('.')
    vkdate.reverse()
    vkdate[1] = vkdate[1] if len(vkdate[1]) == 2 else '0' + vkdate[1]
    vkdate[2] = vkdate[2] if len(vkdate[2]) == 2 else '0' + vkdate[2]
    return '-'.join(vkdate)