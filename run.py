__author__ = 'sashgorokhov'

import modules
import modules.server

application = modules.server.application

import bottle

bottle.run(host=modules.config['server']['ip'], port=modules.config['server']['port'])