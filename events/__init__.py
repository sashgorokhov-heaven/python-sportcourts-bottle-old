events_list = list()

from .game_notifier_2_days import GameNotifier
from .game_notifier_1_day import GameNotifier as GameNotifier2

events_list.append(GameNotifier())
events_list.append(GameNotifier2())

