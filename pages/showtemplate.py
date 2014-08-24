import bottle

import pages


class ShowTemplate(pages.Page):
    @pages.setlogin
    def get(self):
        if 'name' not in bottle.request.query or pages.getadminlevel() != 1:
            raise bottle.HTTPError(404)
        return pages.Template(bottle.request.query.get("name"))

    get.route = '/showtpl'