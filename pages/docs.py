import pages


class Docs(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('docs')

    get.route = '/docs'