import pages


class Admin(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('admin')

    get.route = '/admin'