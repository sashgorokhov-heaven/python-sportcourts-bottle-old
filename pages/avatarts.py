import os

from PIL import Image
import bottle

import pages


class Avatars(pages.Page):
    path = ['avatars']

    def execute(self, method:str):
        if method == 'POST': return self.post()

    def post(self):
        filename = str(bottle.request.forms.get('user_id')) + '.jpg'
        dirname = '/apiserver/data/avatars'
        fullname = os.path.join(dirname, filename)
        if bottle.request.files.get('image').content_length > 5242880:
            raise bottle.HTTPError(404)
        if os.path.splitext(bottle.request.files.get('image').filename)[-1] not in {'.jpg', '.jpeg'}:
            raise bottle.HTTPError(404)
        if os.path.exists(fullname):
            os.remove(fullname)
        bottle.HTTPError(404).save(fullname)
        Image.open(fullname).crop().resize((128, 128)).save(fullname)
        return bottle.redirect('/profile')