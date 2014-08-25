import bottle

import pages


class ShowTemplate(pages.Page):
    def get(self):
        if 'name' not in bottle.request.query or not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)
        return pages.PageBuilder(bottle.request.query.get("name"))

    get.route = '/showtpl'