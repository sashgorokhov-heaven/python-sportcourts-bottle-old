import pages


class Finances(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('finances')

    get.route = '/fin'