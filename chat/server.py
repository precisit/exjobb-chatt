import tornado.ioloop
import tornado.web
import tornado.websocket
import sys
import tornado.log

class EchoWebSocket(websocket.WebSocketHandler):
	def open(self):
		print "Websocket opened."

	def on_message(self,message):
		self.write_message(u"You said: " + message)

	def on_close(self):
		print "Websocket closed."

	def check_origin(self,origin):
		return True



