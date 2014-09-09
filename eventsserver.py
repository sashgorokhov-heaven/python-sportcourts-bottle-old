import bottle, sys, eventslib

config = sys.argv[1]


@bottle.get('/stop')
def stop():
    eventslib.event_server.stop()


eventslib.event_server.start()

application = bottle.default_app()
