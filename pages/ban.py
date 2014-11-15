import bottle
import pages
from models import users


@pages.get('/ban')
@pages.only_admins
def get_ban():
    if 'user_id' not in bottle.request.query:
        raise bottle.HTTPError(404)
    user = users.get(int(bottle.request.query.get('user_id')))
    return pages.PageBuilder('ban', user=user)


@pages.post('/ban')
@pages.only_admins
def post_ban():
    raise NotImplementedError