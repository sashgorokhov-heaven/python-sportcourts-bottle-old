import pages
from models import users

class Users(pages.Page):
    def get(self):
        allusers = users.get(0, detalized=True)
        page = pages.PageBuilder('users', allusers=allusers)
        if pages.auth_dispatcher.loggedin():
            friends = users.get(users.get(pages.auth_dispatcher.getuserid(), fields=['friends'])['friends']['users'],
                                detalized=True)
            page.add_param('myfriends', friends)
        return page

    get.route = '/users'