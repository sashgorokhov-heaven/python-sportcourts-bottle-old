import bottle

import pages


class Index(pages.Page):
    path = ['/', '', 'main']

    def __init__(self):
        pass

    def execute(self, method:str):
        return self.get().template()

    @pages.setlogin
    @pages.handleerrors('index')
    def get(self):
        return bottle.template('index')
