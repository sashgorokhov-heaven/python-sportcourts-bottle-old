import bottle

import modules
import modules.eventslib

bottle.TEMPLATE_PATH.append('views')
bottle.debug(modules.config['debug'])

import pages


@bottle.error(404)
def error404(error):
    return pages.PageBuilder('404').template()


application = bottle.default_app()

bottle.install(modules.exec_time_measure)

import events

for event in events.events_list:
    modules.eventslib.event_server.add_event(event)

modules.eventslib.event_server.start()
