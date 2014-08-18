__author__ = 'sashgorokhov'

import modules.server

application = modules.server.application

import bottle

bottle.run(host=modules.server.config['server']['ip'], port=modules.server.config['server']['port'])