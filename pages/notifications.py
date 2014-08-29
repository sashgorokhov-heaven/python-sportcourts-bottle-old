import bottle

import pages
import modules.dbutils
import models.notifications


class Notifications(pages.Page):
    def get(self):
        if not pages.auth_dispatcher.loggedin():
            raise pages.PageBuilder('text', message='Ошибка доступа',
                                    description='Вы должны войти чтобы просматривать эту страницу')
        user_id = pages.auth_dispatcher.getuserid()
        with modules.dbutils.dbopen() as db:
            count = models.notifications.get_count(user_id, dbconnection=db)
            if count > 0:
                notifications = models.notifications.get(user_id, dbconnection=db)
            else:
                notifications = models.notifications.get(user_id, all=True, dbconnection=db)
        return pages.PageBuilder("notifications", notifications=notifications, all=count == 0)

    def post(self):
        if 'id' not in bottle.request.forms:
            raise bottle.HTTPError(404)
        notification_id = int(bottle.request.forms.get('id'))
        models.notifications.read(notification_id)

    get.route = '/notifications'
    post.route = '/notifications'
