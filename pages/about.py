import pages


class About(pages.Page):
    path = ['about']

    def execute(self, method:str):
        return self.get().template()

    @pages.setlogin
    def get(self):
        return pages.Template('about')