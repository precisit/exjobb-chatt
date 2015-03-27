import tornado.web

class PingHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('pong')

class HejHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('Hello World')

