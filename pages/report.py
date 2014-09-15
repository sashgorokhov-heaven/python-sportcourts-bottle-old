import base64
import json
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
        game = games.get_by_id(game_id, detalized=True)
        game['parsed_datetime'] = (beautifuldate(game['datetime']),
                                   beautifultime(game['datetime']),
                                   beautifulday(game['datetime']))
        # TODO: прошла игра или нет
        return pages.PageBuilder("report", game=game, showreport=game['report']['reported'])

    def post(self):
        if not pages.auth_dispatcher.loggedin() or not pages.auth_dispatcher.responsible():
            return pages.PageBuilder('text', message='Недостаточно плав',
                                     description='Вы не можете просматривать эту страницу')
        users = {int(user_id.split('=')[-1]): {"status": bottle.request.forms.get(user_id)} for user_id in
                 filter(lambda x: x.startswith("status"), bottle.request.forms)}
        registered = {user_id: users[user_id] for user_id in filter(lambda x: x > 0, users)}
        unregistered = {user_id: users[user_id] for user_id in filter(lambda x: x < 0, users)}
        for user_id in unregistered:
            info = {key.split('=')[0]: bottle.request.forms.get(key) for key in
                    filter(lambda x: x.endswith(str(user_id)), bottle.request.forms)}
            unregistered[user_id] = info
        report = {"reported": True}
        report['registered'] = {'count': len(registered), 'users': registered}
        report['unregistered'] = {'count': len(unregistered), 'users': unregistered}
        for user_id in report['unregistered']['users']:
            user = report['unregistered']['users'][user_id]
            user['first_name'] = base64.b64encode(user['first_name'].encode()).decode()
            user['last_name'] = base64.b64encode(user['last_name'].encode()).decode()
        game_id = int(bottle.request.forms.get('game_id'))
        jsondumped = json.dumps(report)
        games.update(game_id, report=jsondumped)
        raise bottle.redirect('/report?game_id={}'.format(game_id))

    get.route = '/report'
    post.route = get.route