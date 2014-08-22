import pages
import modules.dbutils


class Notifications(pages.Page):
    path = ['notifications']

    def execute(self, method:str):
        if method == 'GET':
            return self.get().template()

    @pages.setlogin
    def get(self):
        notifications = pages.get_notifications(pages.getuserid())
        for i in notifications:
            modules.dbutils.strdates(i)
        return pages.Template("notifications", notifications=notifications)

