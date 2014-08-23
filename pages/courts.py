import pages


class Courts(pages.Page):
    path = ['courts']

    @pages.setlogin
    def get(self):
        pass

    def post(self):
        pass
