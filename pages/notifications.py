import bottle

import pages
import modules.dbutils


class Notifications(pages.Page):
    path = ['notifications']

    def execute(self, method:str):
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    @pages.setlogin
    def get(self):
        if not pages.loggedin():
            return bottle.HTTPError(404)
        notifications = pages.get_notifications(pages.getuserid())
        for i in notifications:
            modules.dbutils.strdates(i)
        return pages.Template("notifications", notifications=notifications)

