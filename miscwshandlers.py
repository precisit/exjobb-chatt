import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
	    return True
    
	def open(self):
		print 'En socket oppnades'

	def on_message(self, message):
		self.write_message("You said " + message)

	def on_close(self):
		print 'En socket stangdes'

