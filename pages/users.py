import bottle

import dbutils
import modules
import pages
from models import users


USERS_PER_PAGE = 8


class Users(pages.Page):
    def get(self):
        with dbutils.dbopen() as db:
            count = db.execute("SELECT COUNT(user_id) FROM users WHERE activated=1")[0][0]
            allusers = users.get(0, activated=1, count=slice(*modules.pager(1, count=USERS_PER_PAGE)))
            page = pages.PageBuilder('users', allusers=allusers, count=count)
            if pages.auth.loggedin():
                if len(pages.auth.current().friends()) > 0:
                    friends = pages.auth.current().friends(True)
                    page.add_param('myfriends', friends)
            return page

    def post(self):
        if bottle.request.is_ajax:
            section = bottle.request.forms.get("section")
            startfrom = int(bottle.request.forms.get("startfrom"))
            data = list()
            if section == 'all':
                with dbutils.dbopen() as db:
                    allusers = users.get(0, activated=1,  count=slice(startfrom, USERS_PER_PAGE), dbconnection=db)
                    page = pages.PageBuilder('user_row')
                    if pages.auth.loggedin():
                        if len(pages.auth.current().friends()) > 0:
                            friends = pages.auth.current().friends(True)
                            page.add_param('myfriends', friends)
                    for user in allusers:
                        page.add_param('user', user)
                        user_tpl = page.template()
                        data.append(user_tpl)
                    return bottle.json_dumps(data)
            return ''
        else:
            if 'search' in bottle.request.forms:
                query = bottle.request.forms.get('q')
                with dbutils.dbopen() as db:
                    allusers = users.search(query, dbconnection=db)
                    page = pages.PageBuilder('users', allusers=users.get(allusers, activated=1, dbconnection=db),
                                             count=len(allusers),
                                             search=True, search_q=bottle.request.forms.get('q'))
                    if pages.auth.loggedin() and len(pages.auth.current().friends()) > 0:
                        friends = pages.auth.current().friends(True)
                        page.add_param('myfriends', friends)
                    return page

    get.route = '/users'
    post.route = get.route