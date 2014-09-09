import bottle, sys, eventslib

config = sys.argv[1]

eventslib.event_server.start()

application = bottle.default_app()
