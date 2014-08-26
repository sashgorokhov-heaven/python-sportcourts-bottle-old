import threading
import time

from modules import utils, logging
import modules


TICKTIME = 60  # in secs


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


    @utils.threaded
    def _loop(self):
        while not self._stop:
            self.check_events()
            time.sleep(TICKTIME)

    @utils.threaded
    def check_events(self):
        with self._lock:
            for event in self._eventlist:
                try:
                    if event.condition():
                        self._event_execute(event)
                except Exception as e:
                    logging.error('Event error ' + event.__class__.__name__ + ' - ' + e.__class__.__name__ + ': {}',
                                  str(e.args))
                    logging.info(modules.extract_traceback(e))

    @utils.threaded
    def _event_execute(self, event:Event):
        try:
            event.execute()
        except Exception as e:
            logging.error('Event error ' + event.__class__.__name__ + ' - ' + e.__class__.__name__ + ': {}',
                          str(e.args))
            logging.info(modules.extract_traceback(e))


event_server = _EventServer()