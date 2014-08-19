import pages


class Index(pages.Page):
    path = ['/', '', 'main']

    def execute(self, method:str):
        return self.get().template()

    @pages.setlogin
    @pages.handleerrors('index')
    def get(self):
        return pages.Template('index')
