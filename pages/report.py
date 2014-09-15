import bottle
from modules.utils import beautifuldate, beautifultime, beautifulday
import pages
from models import games

class Report(pages.Page):
    def get(self):
        if 'game_id' not in bottle.request.query:
            raise bottle.HTTPError(404)
        if not pages.auth_dispatcher.loggedin() or not pages.auth_dispatcher.responsible():
            return pages.PageBuilder('text', message='Недостаточно плав',
                                     description='Вы не можете просматривать эту страницу')
        game_id = int(bottle.request.query.get('game_id'))
        report = games.get_report(game_id)
        if report['reported']:
            return self.get_show(game_id, report)
        else:
            # TODO: прошла игра или нет
            return self.get_add(game_id)

    def get_show(self, game_id:int, report:dict):
        pass

    def get_add(self, game_id:int):
        game = games.get_by_id(game_id, detalized=True)
        game['parsed_datetime'] = (beautifuldate(game['datetime']),
                                   beautifultime(game['datetime']),
                                   beautifulday(game['datetime']))
        return pages.PageBuilder("report", game=game)

    get.route = '/report'