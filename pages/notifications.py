import bottle

import pages
import modules.dbutils
import models.notifications


class Notifications(pages.Page):
    def execute(self, method:str, **kwargs):
        if not pages.auth_dispatcher.loggedin():
            return pages.templates.permission_denied().template()
        return super().execute(method, **kwargs)

    def get(self):
        user_id = pages.auth_dispatcher.getuserid()
        with modules.dbutils.dbopen() as db:
            if 'deleteall' in bottle.request.query:
                models.notifications.delete(-user_id)
                raise bottle.redirect('/notifications')
            count = models.notifications.get_count(user_id, dbconnection=db)
            notifications = dict()
            notifications['all'] = models.notifications.get(user_id, type=0, all=count == 0, dbconnection=db)
            notifications['subscribed'] = models.notifications.get(user_id, type=1, all=count == 0, dbconnection=db)
            if pages.auth_dispatcher.responsible() or pages.auth_dispatcher.organizer() or pages.auth_dispatcher.admin():
                notifications['responsible'] = models.notifications.get(user_id, type=2, all=count == 0,
                                                                        dbconnection=db)
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
