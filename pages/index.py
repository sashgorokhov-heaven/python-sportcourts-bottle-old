import pages


class Index(pages.Page):
    path = ['/', '', 'main']


    @pages.setlogin
    @pages.handleerrors('index')
    def get(self):
        return pages.Template('index')
