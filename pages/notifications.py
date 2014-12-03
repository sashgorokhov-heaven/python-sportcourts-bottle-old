import bottle
import pages
import dbutils
import models.notifications
import cacher

@pages.get('/notifications')
@pages.only_loggedin
def get():
    user_id = pages.auth.current().user_id()
    with dbutils.dbopen() as db:
        if 'deleteall' in bottle.request.query:
            models.notifications.delete(-user_id)
            raise bottle.redirect('/notifications')
        count = models.notifications.get_count(user_id, dbconnection=db)
        notifications = dict()
        notifications['all'] = models.notifications.get(user_id, type=0, all=count == 0, dbconnection=db)
        notifications['subscribed'] = models.notifications.get(user_id, type=1, all=count == 0, dbconnection=db)
        if pages.auth.current().userlevel.resporgadmin():
            notifications['responsible'] = models.notifications.get(user_id, type=2, all=count == 0,
                                                                    dbconnection=db)
        return pages.PageBuilder("notifications", notifications=notifications, all=count == 0)


@pages.post('/notifications')
@pages.only_loggedin
def post():
    if 'read' in bottle.request.forms:
        notification_id = int(bottle.request.forms.get('read'))
        models.notifications.read(notification_id)
        cacher.drop('notifications_count', pages.auth.current().user_id())
    if 'delete' in bottle.request.forms:
        notification_id = int(bottle.request.forms.get('delete'))
        models.notifications.delete(notification_id)
        cacher.drop('notifications_count', pages.auth.current().user_id())