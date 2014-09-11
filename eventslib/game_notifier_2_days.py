from modules import dbutils, time
from models import notifications
import eventslib

BUFFERLIFE = 60 * 30  # 15 minutes


class GameNotifier(eventslib.Event):
    def __init__(self):
        self._condition_value = list()
        self._notified = set()

    def condition(self):
        with dbutils.dbopen() as db:
            db.execute(
                "SELECT * FROM games WHERE datetime BETWEEN NOW() + INTERVAL 2 DAY - INTERVAL 5 MINUTE AND NOW() + INTERVAL 2 DAY + INTERVAL 5 MINUTE",
                dbutils.dbfields['games'])
            if len(db.last()) == 0:
                return False
            self._condition_value = db.last()
            return True

    def execute(self):
        for game in self._condition_value:
            game['subscribed'] = list(
                filter(lambda x: x != '', map(lambda x: x.strip(), game['subscribed'].split(','))))
            if len(game['subscribed']) == 0:
                continue
            for user_id in game['subscribed']:
                if (user_id, game['game_id']) not in {i[:2] for i in self._notified}:
                    message = 'До игры "{}" осталось 2 дня!'.format(
                        '<a href="/games?game_id={}">#{} | {}</a>'.format(
                            game['game_id'],
                            game['game_id'],
                            game['description'])
                    )
                    print(ascii(message))
                    notifications.add(user_id, message.replace('"', '\"'))
                    self._notified.add((user_id, game['game_id'], time.time()))
        self._notified = set(filter(lambda x: time.time() - x[-1] < BUFFERLIFE, self._notified))