import pages


class About(pages.Page):
    path = ['about']

    @pages.setlogin
    def get(self):
        return pages.Template('about')