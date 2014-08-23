import bottle

import pages


class ShowTemplate(pages.Page):
    path = ['showtpl']

    def execute(self, method:str):
        if method == 'GET':
            data = self.get()
            if isinstance(data, pages.Template):
                return data.template()
            return data

    @pages.setlogin
    def get(self):
        if 'name' not in bottle.request.query or pages.getadminlevel() != 1:
            raise bottle.HTTPError(404)
        return pages.Template(bottle.request.query.get("name"))
