import bottle
from modules import dbutils
import modules
import pages
from models import users


USERS_PER_PAGE = 8


class Users(pages.Page):
    def get(self):
        with dbutils.dbopen() as db:
            paging = {'previous': 0, 'next': 0}
            count = int(db.execute("SELECT COUNT(user_id) FROM users")[0][0])
            total_pages = count // USERS_PER_PAGE + 1
            page_n = 1
            if 'page' in bottle.request.query:
                page_n = int(bottle.request.query.get('page'))
                if not 0 < page_n <= total_pages:
                    raise bottle.HTTPError(404)
                if page_n != total_pages:
                    paging['next'] = page_n + 1
                if page_n > 1:
                    paging['previous'] = page_n - 1
            else:
                if total_pages > 1:
                    paging['next'] = 2
            allusers = users.get(0, count=slice(*modules.pager(page_n, count=USERS_PER_PAGE)), detalized=True)
            page = pages.PageBuilder('users', allusers=allusers, paging=paging)
            if pages.auth_dispatcher.loggedin():
                friends = users.get(
                    users.get(pages.auth_dispatcher.getuserid(), fields=['friends'])['friends']['users'],
                    detalized=True)
                page.add_param('myfriends', friends)
        return page

    get.route = '/users'