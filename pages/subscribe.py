import bottle

import pages
import modules.dbutils


class Subscribe(pages.Page):
    path = ['subscribe']

    def execute(self, method:str):
        params = {i: bottle.request.forms[i] for i in bottle.request.forms} if method == 'POST' else {
        i: bottle.request.query.get(i) for i in bottle.request.query}
        return self.post(params)

    def post(self, params:dict=None):
        """
        game_id
        [unsubscribe]
        [fromedit]
        """
        with modules.dbutils.dbopen() as db:
            db.execute("SELECT subscribed FROM games WHERE game_id={}".format(params['game_id']))
            if len(db.last()) == 0:
                raise bottle.HTTPError(404)
            data = db.last()[0][0]
            if 'unsubscribe' not in params:
                if data:
                    if str(pages.getuserid()) in data:
                        raise bottle.HTTPError(404)
                    else:
                        data = ','.join(data.split(',') + [str(pages.getuserid())])
                else:
                    data = str(pages.getuserid())
            else:
                if data:
                    if str(pages.getuserid()) in data:
                        data = data.split(',')
                        data.remove(str(pages.getuserid()))
                        data = ','.join(data)
                    else:
                        raise bottle.HTTPError(404)
                else:
                    raise bottle.HTTPError(404)
            db.execute(
                "UPDATE games SET subscribed='{}' WHERE game_id={}".format(data, params['game_id']))
            if 'fromedit' in params:
                raise bottle.redirect('/games?edit={}'.format(params['game_id']))
            return ''