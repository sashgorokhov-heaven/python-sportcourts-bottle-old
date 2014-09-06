import json
from models import autodb
from modules import dbutils


class SettingsClass(dict):
    def __init__(self, data=None):
        super().__init__()
        if data:
            self._settings = json.loads(data)
        else:
            self._settings = dict()

    def _get(self, key:str):
        return self._settings[key] if key in self._settings else False

    def _set(self, key:str, value):
        self._settings[key] = value

    def send_email(self, value=None) -> bool:
        if value:
            self._set('send_mail', value)
        else:
            return self._get('send_mail')

    def show_phone(self, value=None):
        if value:
            self._set('show_phone', value)
        else:
            return self._get('show_phone')

    def __getitem__(self, item):
        return self._get(item)

    def __setitem__(self, key, value):
        return self._set(key, value)

    def format(self):
        return json.dumps(self._settings)

    def __str__(self):
        return str(self._settings)


def default() -> SettingsClass:
    settings = SettingsClass()
    settings.send_email(True)
    settings.show_phone('all')
    return settings


@autodb
def get(user_id:int, dbconnection:dbutils.DBConnection=None) -> SettingsClass:
    dbconnection.execute("SELECT settings FROM users WHERE user_id={}".format(user_id))
    return SettingsClass(dbconnection.last()[0][0])


@autodb
def set(user_id:int, settings:SettingsClass, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("UPDATE users SET settings='{}' WHERE user_id={}".format(settings.format(), user_id))

