import bottle

import pages
from models import games, notifications


class Subscribe(pages.Page):
    def post(self):
        """
        game_id
        [unsubscribe]
        """
        if not pages.auth_dispatcher.loggedin():
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.forms.get('game_id'))
        user_id = int(pages.auth_dispatcher.getuserid())
        unsubscribe = 'unsubscribe' in bottle.request.forms

        try:
            if unsubscribe:
                games.unsubscribe(user_id, game_id)
            else:
                games.subscribe(user_id, game_id)
        except ValueError:
            pass

    def get(self):
        """
        game_id
        user_id
        [unsubscribe]
        """
        if not pages.auth_dispatcher.organizer():
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.query.get('game_id'))
        user_id = int(bottle.request.query.get('user_id'))
        unsubscribe = 'unsubscribe' in bottle.request.query

        try:
            if unsubscribe:
                games.unsubscribe(user_id, game_id)
            else:
                games.subscribe(user_id, game_id)
        except ValueError:
            pass

        notifications.add(user_id,
                          'Вы были удалены с игры "<a href="/games?game_id={}">#{} | {}</a>"'.format(
                              game_id, game_id,
                              games.get_by_id(game_id, fields=['description'])['description']),
                          1)

        raise bottle.redirect('/games?edit={}'.format(game_id))

    post.route = '/subscribe'
    get.route = post.route