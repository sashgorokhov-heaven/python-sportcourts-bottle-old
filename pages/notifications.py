import bottle

import pages
import modules.dbutils
import models.notifications


class Notifications(pages.Page):
    def get(self):
        if not pages.auth_dispatcher.loggedin():
            return pages.PageBuilder('text', message='Ошибка доступа',
                                    description='Вы должны войти чтобы просматривать эту страницу')
        user_id = pages.auth_dispatcher.getuserid()
        with modules.dbutils.dbopen() as db:
            if 'deleteall' in bottle.request.query:
                models.notifications.delete(-user_id, dbconnection=db)
            count = models.notifications.get_count(user_id, dbconnection=db)
            if count > 0:
                notifications = models.notifications.get(user_id, dbconnection=db)
            else:
                notifications = models.notifications.get(user_id, all=True, dbconnection=db)
        return pages.PageBuilder("notifications", notifications=notifications, all=count == 0)

    def post(self):
        if 'read' in bottle.request.forms:
            notification_id = int(bottle.request.forms.get('read'))
            models.notifications.read(notification_id)
        if 'delete' in bottle.request.forms:
            notification_id = int(bottle.request.forms.get('delete'))
            models.notifications.delete(notification_id)


    get.route = '/notifications'
    post.route = '/notifications'
