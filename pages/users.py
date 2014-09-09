import pages


class Users(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('users')

    get.route = '/users'