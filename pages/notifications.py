import bottle

from modules.utils import beautifuldate, beautifultime, get_notifications
import pages
import modules.dbutils


class Notifications(pages.Page):
    @pages.setlogin
    def get(self):
        if not pages.loggedin():
            return bottle.HTTPError(404)
        notifications = get_notifications(pages.getuserid())
        for i in notifications:
            modules.dbutils.strdates(i)
            i['datetime'] = '{} {}'.format(beautifuldate(i['datetime']), beautifultime(i['datetime']))
        return pages.Template("notifications", notifications=notifications)

    get.route = '/notifications'
