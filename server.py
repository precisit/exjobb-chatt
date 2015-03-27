import tornado.ioloop 
import tornado.web
import tornado.websocket
import tornado.log

tornado.log.enable_pretty_logging()

import mischandlers
import miscwshandlers

application = tornado.web.Application([
	(r"/", mischandlers.PingHandler),
	(r"/hej", mischandlers.HejHandler),
	(r"/echoSocket", miscwshandlers.EchoWebSocket),
], autoreload=True, debug=True)

application.listen(1080)
tornado.ioloop.IOLoop.instance().start()
	