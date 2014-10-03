import base64
import datetime
import json
import bottle
from modules.utils import beautifuldate, beautifultime, beautifulday
import pages
from modules import dbutils, create_link
from models import games, images, notifications, users, usergames


class Report(pages.Page):
    def get(self):
        if 'game_id' not in bottle.request.query:
            raise bottle.HTTPError(404)
        game_id = int(bottle.request.query.get('game_id'))
        with dbutils.dbopen() as db:
            game = games.get_by_id(game_id, detalized=True, dbconnection=db)
            if len(game) == 0:
                raise bottle.HTTPError(404)
            game['parsed_datetime'] = (beautifuldate(game['datetime']),
                                       beautifultime(game['datetime']),
                                       beautifulday(game['datetime']))
            if game['created_by']['user_id'] != pages.auth_dispatcher.getuserid() and game['responsible_user'][
                'user_id'] != pages.auth_dispatcher.getuserid() and not pages.auth_dispatcher.admin():
                return pages.templates.permission_denied()
            if datetime.datetime.now()<game['datetime_pure']+datetime.timedelta(minutes=game['duration']):
                return pages.templates.message("Вы не можете отправить отчет по игре", "Игра еще не закончилась")
            return pages.PageBuilder("report", game=game, showreport=game['report']['reported'])

    def post(self):
        game_id = int(bottle.request.forms.get('game_id'))
        game = games.get_by_id(game_id, fields=['game_id', 'responsible_user_id', 'created_by', 'description'])
        if game['created_by'] != pages.auth_dispatcher.getuserid() and game[
            'responsible_user_id'] != pages.auth_dispatcher.getuserid() and not pages.auth_dispatcher.admin():
            return pages.templates.permission_denied()
        users_ = {int(user_id.split('=')[-1]): {"status": bottle.request.forms.get(user_id)} for user_id in
                 filter(lambda x: x.startswith("status"), bottle.request.forms)}
        registered = {user_id: users_[user_id] for user_id in filter(lambda x: x > 0, users_)}
        unregistered = {user_id: users_[user_id] for user_id in filter(lambda x: x < 0, users_)}
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
        jsondumped = json.dumps(report)
        games.update(game_id, report=jsondumped)
        if "photo" in bottle.request.files:
            images.save_report(game_id, bottle.request.files.get("photo"))
        if pages.auth_dispatcher.getuserid() != game['created_by']:
            notifications.add(game['created_by'], 'Ответственный "{}" отправил отчет по игре "{}"'.format(
                create_link.user(
                    users.get(pages.auth_dispatcher.getuserid(), fields=['user_id', 'first_name', 'last_name'])),
                create_link.game(game)), game_id, 2)
        self.report_users(game_id, report['registered']['users'])
        raise bottle.redirect('/report?game_id={}'.format(game_id))

    def report_users(self, game_id:int, users:dict):
        with dbutils.dbopen() as db:
            for user_id in users:
                usergames.set(int(user_id), game_id, int(users[user_id]['status']), dbconnection=db)


    get.route = '/report'
    post.route = get.route