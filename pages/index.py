import pages


class Index(pages.Page):
    def get(self):
        return pages.PageBuilder('index')

    get.route = '/'