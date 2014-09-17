import base64
import json
import bottle
from modules.utils import beautifuldate, beautifultime, beautifulday
import pages
from models import games

class List(pages.Page):
    def get(self):
        if 'game_id' not in bottle.request.query:
            raise bottle.HTTPError(404)
        if not pages.auth_dispatcher.loggedin() or not pages.auth_dispatcher.responsible():
            return pages.PageBuilder('text', message='Недостаточно плав',
                                     description='Вы не можете просматривать эту страницу')
        game_id = int(bottle.request.query.get('game_id'))
        game = games.get_by_id(game_id, detalized=True)
        game['parsed_datetime'] = (beautifuldate(game['datetime']),
                                   beautifultime(game['datetime']),
                                   beautifulday(game['datetime']))
        # TODO: прошла игра или нет
        return pages.PageBuilder("report", game=game, showreport=game['report']['reported'])

    get.route = '/list'
    post.route = get.route