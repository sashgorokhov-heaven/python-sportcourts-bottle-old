import bottle
import pages
from modules import dbutils
from models import games

class List(pages.Page):
    def get(self, game_id:int):
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, detalized=True, dbconnection=db)
            if len(game) == 0:
                raise bottle.HTTPError(404)
            if pages.auth_dispatcher.getuserid() != game['created_by'][
                'user_id'] and pages.auth_dispatcher.getuserid() != game['responsible_user'][
                'user_id'] and not pages.auth_dispatcher.admin():
                return pages.templates.permission_denied()
            return pages.PageBuilder('list', game=game)

    get.route = '/list/<game_id:int>'