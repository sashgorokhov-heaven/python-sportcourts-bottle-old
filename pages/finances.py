import pages


class Finances1(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('finances')

    get.route = '/fin1'