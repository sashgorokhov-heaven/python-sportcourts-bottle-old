import bottle

import dbutils
import pages
from models import games


class List(pages.Page):
    def get(self, game_id:int):
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, dbconnection=db)
            if len(game) == 0:
                raise bottle.HTTPError(404)
            if pages.auth.current().user_id() != game.created_by() and pages.auth.current().user_id() != game.responsible_user_id() and not pages.auth.current().userlevel.admin():
                return pages.templates.permission_denied()
            return pages.PageBuilder('list', game=game)

    get.route = '/list/<game_id:int>'