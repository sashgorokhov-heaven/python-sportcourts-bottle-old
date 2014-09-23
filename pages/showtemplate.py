import bottle

import pages


class ShowTemplate(pages.Page):
    def get(self, name:str):
        if not pages.auth_dispatcher.admin():
            raise bottle.HTTPError(404)
        return pages.PageBuilder(name)

    get.route = '/showtpl/<name:str>'