import os
import bottle
import config
import pages
from models import games


@pages.get('/images/avatars/<name>')
def get_avatar_image(name):
    filename = str(name)
    dirname = config.paths.images.avatars
    fullaname = os.path.join(dirname, filename + '.jpg')
    if not os.path.exists(fullaname):
        filename = 'blank'
        return bottle.static_file('{}.jpg'.format(filename), dirname), os.path.join(dirname,
                                                                                    '{}.jpg'.format(filename))
    if 'sq' in bottle.request.query:
        filename += '_sq'
    elif 'sq_sm' in bottle.request.query:
        filename += '_sq_sm'
    if not os.path.exists(os.path.join(dirname, filename + '.jpg')):
        filename = 'blank'
        return bottle.static_file('{}.jpg'.format(filename), dirname), os.path.join(dirname,
                                                                                    '{}.jpg'.format(filename))
    return bottle.static_file('{}.jpg'.format(filename), dirname), os.path.join(dirname, '{}.jpg'.format(filename))


@pages.get('/images/og/<name>')
def get_og_image(name):
    return bottle.static_file(name, config.paths.images.og)


@pages.get('/images/reports/<game_id>')
@pages.only_loggedin
def get_report_image(game_id):
    game = games.get_by_id(game_id)
    if pages.auth.current().user_id() == game.responsible_user_id() or pages.auth.current().user_id() == \
            game.created_by() or pages.auth.current().userlevel.admin():
        return bottle.static_file(game_id + '.jpg', config.paths.images.reports)
    raise bottle.HTTPError(404)
