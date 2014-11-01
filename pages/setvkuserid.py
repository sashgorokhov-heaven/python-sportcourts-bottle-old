import bottle
import pages
from models import users
from modules import vk

class SetVkUserId(pages.Page):
    def get(self, **kwargs):
        if 'code' not in bottle.request.query or not pages.auth.loggedin():
            raise bottle.HTTPError(404)
        code = bottle.request.query.get('code')
        try:
            access_token, user_id, email = vk.auth_code(code, '/setvkid')
        except ValueError as e:
            return pages.templates.message(error=e.vkerror['error'], error_description=e.vkerror['error_description'])
        users.setvkuserid(pages.auth.current().user_id(), int(user_id))
        raise bottle.redirect('/profile')


    get.route = '/setvkid'