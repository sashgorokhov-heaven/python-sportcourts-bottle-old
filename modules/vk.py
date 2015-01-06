import json
import urllib.request
import urllib.parse, urllib.error
import http.cookiejar, html.parser

import bottle

import config


def exec(token, method:str, **kwargs) -> dict:
    params = list()
    for key in kwargs:
        if len(str(kwargs[key])) != 0:
            if isinstance(kwargs[key], list):
                params.append((key, ','.join(map(str, kwargs[key]))))
            else:
                params.append((key, str(kwargs[key])))
    if token:
        params.append(("access_token", token))
    params.append(('v', '5.27'))
    url = 'https://api.vk.com/method/{0}?{1}'.format(method, urllib.parse.urlencode(params))
    response = urllib.request.urlopen(url).read().decode()
    response = json.loads(response)
    return response['response']


def auth_code(code:str, redirec_page:str) -> (str, int, str):
    url = "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&code={2}&redirect_uri=http://{3}:{4}" + redirec_page
    url = url.format(config.vk.appid, config.vk.secret, code, config.server.ip, config.server.port)
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
    vkdate[0] = vkdate[0] if len(vkdate[0]) == 2 else '0' + vkdate[0]
    vkdate[1] = vkdate[1] if len(vkdate[1]) == 2 else '0' + vkdate[1]
    return '.'.join(vkdate)


class VKAuthError(Exception): pass


class _FormParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = 'GET'

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'form':
            if self.form_parsed:
                raise VKAuthError('Second form on page')
            if self.in_form:
                raise VKAuthError('Already in form')
            self.in_form = True
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == 'form':
            self.url = attrs['action']
            if 'method' in attrs:
                self.method = attrs['method']
        elif tag == 'input' and 'type' in attrs and 'name' in attrs:
            if attrs['type'] in ['hidden', 'text', 'password']:
                self.params[attrs['name']] = attrs['value'] if 'value' in attrs else ''

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'form':
            if not self.in_form:
                raise VKAuthError('Unexpected end of <form>')
            self.in_form = False
            self.form_parsed = True


def auth(login, passwd, appid, scope):
    if not isinstance(scope, list):
        scope = [scope]

    _opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
        urllib.request.HTTPRedirectHandler())
    try:
        response = _opener.open(
            'http://oauth.vk.com/oauth/authorize?' + \
            'redirect_uri=oauth.vk.com/blank.html&response_type=token&' + \
            'client_id={0}&scope={1}&display=wap'.format(appid, ','.join(scope))
        )
    except urllib.error.URLError as e:
        raise VKAuthError('Cant connect to vk.com or app_id is invalid.')
    except Exception as e:
        raise VKAuthError('Unhandled exception: ' + str(e))

    doc = response.read().decode()
    parser = _FormParser()
    parser.feed(doc)
    parser.close()

    if not parser.form_parsed or parser.url is None or 'pass' not in parser.params or 'email' not in parser.params:
        raise VKAuthError('Unexpected response page o_O')

    parser.params['email'] = login
    parser.params['pass'] = passwd
    parser.method = 'POST'
    keys = [i for i in parser.params]
    for i in keys:
        b = '1'.encode()
        if type(i) != type(b):
            a = i.encode()
        else:
            a = i
        if type(parser.params[i]) != type(b):
            parser.params[a] = parser.params[i].encode()
        else:
            parser.params[a] = parser.params[i]
        parser.params.pop(i)

    response = _opener.open(parser.url, urllib.parse.urlencode(parser.params).encode())

    doc = response.read()
    url = response.geturl()

    if urllib.parse.urlparse(url).path != '/blank.html':
        parser = _FormParser()
        parser.feed(str(doc))
        parser.close()
        if not parser.form_parsed or parser.url is None:
            raise VKAuthError('Invalid email or password')
        if parser.method == 'post':
            response = _opener.open(parser.url, urllib.parse.urlencode(parser.params).encode())
        else:
            raise VKAuthError('Unexpected method: ' + parser.method)
        url = response.geturl()

    if urllib.parse.urlparse(url).path != "/blank.html":
        raise VKAuthError('Invalid email or password')

    answer = dict(tuple(kv_pair.split('=')) for kv_pair in urllib.parse.urlparse(url).fragment.split('&'))
    if 'access_token' not in answer or 'user_id' not in answer:
        raise VKAuthError('Missing some values in answer')

    return answer['access_token'], answer['user_id'], answer['expires_in']