import bottle
import pages
from models import users

class Ban(pages.Page):
    def get(self):
        if 'user_id' not in bottle.request.query:
            raise bottle.HTTPError(404)
        if not pages.auth_dispatcher.admin():
            raise pages.templates.permission_denied()
        user = users.get(int(bottle.request.query.get('user_id')), detalized=True)
        return pages.PageBuilder('ban', user=user)

    def post(self):
        pass

    get.route = '/ban'
    post.route = get.route
