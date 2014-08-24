import pages


class About(pages.Page):
    @pages.setlogin
    def get(self, **kwargs):
        return pages.Template('about')

    get.route = '/about'