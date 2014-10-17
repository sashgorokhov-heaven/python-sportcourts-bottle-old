import bottle

import dbutils
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
            allusers = users.get(0, count=slice(*modules.pager(page_n, count=USERS_PER_PAGE)))
            page = pages.PageBuilder('users', allusers=allusers, paging=paging, count=count)
            if pages.auth.loggedin():
                if len(pages.auth.current().friends())>0:
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
                    allusers = users.get(0, count=slice(startfrom, USERS_PER_PAGE), dbconnection=db)
                    page = pages.PageBuilder('user_row')
                    if pages.auth.loggedin():
                        if len(pages.auth.current().friends())>0:
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
                query = bottle.request.forms.get('q').split(' ')
                query = list(map(lambda x: '%'+x+'%', query))
                with dbutils.dbopen() as db:
                    sql = "SELECT user_id FROM users WHERE "
                    if len(query)==1:
                        sql += "first_name LIKE '{first}' OR last_name LIKE '{first}'".format(first=query[0])
                    else:
                        sql += ("first_name LIKE '{first}' AND last_name LIKE '{last}'"
                                " OR "
                                "first_name LIKE '{last}' AND last_name LIKE '{first}'").format(first=query[0], last=query[1])
                    db.execute(sql)
                    user_ids = list(map(lambda x: x[0], db.last())) if len(db.last())>0 else list()
                    page = pages.PageBuilder('users', allusers=users.get(user_ids, dbconnection=db),
                                             count=len(user_ids),
                                             search=True, search_q=bottle.request.forms.get('q'))
                    if pages.auth.loggedin() and len(pages.auth.current().friends())>0:
                        friends = pages.auth.current().friends(True)
                        page.add_param('myfriends', friends)
                    return page

    get.route = '/users'
    post.route = get.route