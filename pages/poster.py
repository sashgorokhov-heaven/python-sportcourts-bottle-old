import bottle

import pages


class Poster(pages.Page):
    def post(self, **kwargs):
        response = list()
        line = '<p><b>{}:</b>{}</p>'
        for key in bottle.request.forms:
            response.append(line.format(key, ascii(bottle.request.forms.getall(key))))
        response.append('<hr>')
        for file in bottle.request.files:
            response.append(line.format(file, ascii(bottle.request.forms.get(file))))
        return '\n'.join(response)

    post.route = '/poster'
