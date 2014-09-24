import pages


class List(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('list')

    get.route = '/list'