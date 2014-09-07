import models
from modules import dbutils


class SettingsClass(models.JsonDBData):
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


def default() -> SettingsClass:
    settings = SettingsClass()
    settings.send_email(True)
    settings.show_phone('all')
    return settings


@models.autodb
def get(user_id:int, dbconnection:dbutils.DBConnection=None) -> SettingsClass:
    dbconnection.execute("SELECT settings FROM users WHERE user_id={}".format(user_id))
    return SettingsClass(dbconnection.last()[0][0])


@models.autodb
def set(user_id:int, settings:SettingsClass, dbconnection:dbutils.DBConnection=None):
    dbconnection.execute("UPDATE users SET settings='{}' WHERE user_id={}".format(settings.format(), user_id))

