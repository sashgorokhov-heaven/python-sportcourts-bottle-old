import pages


class Commands(pages.Page):
    def get(self, **kwargs):
        pass

    def post(self, **kwargs):
        pass

    get.route = '/commands/<action>/<params>'
    post.route = '/commands/<action>'