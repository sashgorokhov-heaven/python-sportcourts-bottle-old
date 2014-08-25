import pages


class About(pages.Page):
    def get(self, **kwargs):
        return pages.PageBuilder('about')

    get.route = '/about'