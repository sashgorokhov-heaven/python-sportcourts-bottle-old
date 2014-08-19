import bottle

import pages


class Logout(pages.Page):
    path = ['logout']

    def execute(self, method:str):
        return self.get()

    def get(self):
        if pages.loggedin():
            bottle.response.delete_cookie('user_id')
        raise bottle.redirect('/')