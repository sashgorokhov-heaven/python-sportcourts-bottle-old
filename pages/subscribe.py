import bottle

import pages
import modules.dbutils


class Subscribe(pages.Page):
    def post(self):
        """
        game_id
        [unsubscribe]
        [fromedit]
        """
        if not pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        params = {i: bottle.request.forms.get(i) for i in bottle.request.forms}
        with modules.dbutils.dbopen() as db:
            db.execute("SELECT subscribed FROM games WHERE game_id={}".format(params['game_id']))
            if len(db.last()) == 0:
                raise bottle.HTTPError(404)
            data = db.last()[0][0]
            if 'unsubscribe' not in params:
                if data:
                    if str(pages.auth_dispatcher.getuserid()) in data:
                        raise bottle.HTTPError(404)
                    else:
                        data = ','.join(data.split(',') + [str(pages.auth_dispatcher.getuserid())])
                else:
                    data = str(pages.auth_dispatcher.getuserid())
            else:
                if data:
                    if str(pages.auth_dispatcher.getuserid()) in data:
                        data = data.split(',')
                        data.remove(str(pages.auth_dispatcher.getuserid()))
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

    post.route = '/subscribe'