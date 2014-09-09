import threading
import traceback
import time


TICKTIME = 60  # in secs


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=func.__qualname__)
        thread.start()
        return thread

    return wrapper


def extract_traceback(e):
    return '\n'.join(traceback.format_exception(e.__class__, e, e.__traceback__))


class Event:
    def condition(self) -> bool:
        return False

    def execute(self):
        pass


class _EventServer:
    def __init__(self):
        self._eventlist = list()
        self._stop = False
        self._lock = threading.Lock()

    def start(self):
        self._loop()

    def stop(self):
        self._stop = True

    def add_event(self, event:Event):
        with self._lock:
            self._eventlist.append(event)

    @threaded
    def _loop(self):
        while True:
            self.check_events()
            for i in range(TICKTIME):
                if not self._stop:
                    time.sleep(1)
                else:
                    return

    def check_events(self):
        with self._lock:
            for event in self._eventlist:
                try:
                    if event.condition():
                        self._event_execute(event)
                except Exception as e:
                    pass  # TODO: Error handling

    @threaded
    def _event_execute(self, event:Event):
        try:
            event.execute()
        except Exception as e:
            pass  # TODO: Error handling


event_server = _EventServer()

from .game_notifier_2_days import GameNotifier
from .game_notifier_1_day import GameNotifier as GameNotifier2

event_server.add_event(GameNotifier)
event_server.add_event(GameNotifier2)
