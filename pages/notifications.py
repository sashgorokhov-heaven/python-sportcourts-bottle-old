import bottle

from modules.utils import beautifuldate, beautifultime, get_notifications
import pages
import modules.dbutils


class Notifications(pages.Page):
    def get(self):
        if not pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        notifications = get_notifications(pages.auth_dispatcher.getuserid())
        for i in notifications:
            modules.dbutils.strdates(i)
            i['datetime'] = '{} {}'.format(beautifuldate(i['datetime']), beautifultime(i['datetime']))
        return pages.PageBuilder("notifications", notifications=notifications)

    get.route = '/notifications'
