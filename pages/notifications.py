import bottle

import pages
import modules.dbutils
from modules import beautifuldate, beautifultime, get_notifications


class Notifications(pages.Page):
    path = ['notifications']

    @pages.setlogin
    def get(self):
        if not pages.loggedin():
            return bottle.HTTPError(404)
        notifications = get_notifications(pages.getuserid())
        for i in notifications:
            modules.dbutils.strdates(i)
            i['datetime'] = '{} {}'.format(beautifuldate(i['datetime']), beautifultime(i['datetime']))
        return pages.Template("notifications", notifications=notifications)

