import tornado.ioloop
import tornado.web
import tornado.websocket
import sys
import tornado.log

from tornado.options import define, options
define("port", default=3000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

class MainHandler(tornado.web.RequestHandler):
	def get(self):
	 	self.write("message")

class EchoWebSocket(websocket.WebSocketHandler):
	def open(self):
		router.addConnection(self)
		self.write_message('Welcome to Siris and Kerstins chat')
		print "Websocket opened."

	def on_message(self,message):
		for client in clients
		self.write_message(u"You said: " + message)

	def on_close(self):
		router.removeConnection(self)
		print "Websocket closed."

	def check_origin(self,origin):
		return True

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler)
])

if __name__ == "__main__":
    application.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
