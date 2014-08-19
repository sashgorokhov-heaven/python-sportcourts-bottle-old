import bottle

import pages
import modules.dbutils


class Subscribe(pages.Page):
    path = ['subscribe']

    def execute(self, method:str):
        return self.get()

    def get(self):
        """
        user_id
        game_id
        [unsubscribe]
        """
        with modules.dbutils.dbopen() as db:
            db.execute("SELECT subscribed FROM games WHERE game_id={}".format(bottle.request.query.get('game_id')))
            if len(db.last()) == 0:
                raise bottle.HTTPError(404)
            data = db.last()[0][0]
            if 'unsubscribe' not in bottle.request.query:
                if data:
                    if bottle.request.query.get('user_id') in data:
                        raise bottle.HTTPError(404)
                    else:
                        data = ','.join(data.split(',') + [bottle.request.query.get('user_id')])
                else:
                    data = bottle.request.query.get('user_id')
            else:
                if data:
                    if bottle.request.query.get('user_id') in data:
                        data = data.split(',')
                        data.remove(bottle.request.query.get('user_id'))
                        data = ','.join(data)
                    else:
                        raise bottle.HTTPError(404)
                else:
                    raise bottle.HTTPError(404)
            db.execute(
                "UPDATE games SET subscribed='{}' WHERE game_id={}".format(data, bottle.request.query.get('game_id')))
            return ''