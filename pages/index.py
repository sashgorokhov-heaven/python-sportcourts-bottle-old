import pages


class Index(pages.Page):
    @pages.setlogin
    def get(self):
        return pages.Template('index')

    get.route = '/'