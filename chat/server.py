import tornado.ioloop
import tornado.web
import tornado.websocket
import sys
import tornado.log
# import logging

import router
from messagehandling import PikaClient

from tornado.options import define, options

tornado.log.enable_pretty_logging()

# define("port", default=3000, help="run on the given port", type=int)
# define("debug", default=False, help="run in debug mode")

class MainHandler(tornado.web.RequestHandler):
	def get(self):
	 	self.write("Hello world")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		router.addConnection(self) # Connect to router
		self.write_message('New client connected')
		print "You are connected."

#class BaseHandler(tornado.web.RequestHandler):
 #   def _handle_request_exception(self, e):
  #      logging.error('error')

	def on_message(self,message):
		router.handleMessage()
		# for client in clients
		# self.write_message(u"You said: " + message)
		# anropa den funktion i messagehandler som 
		# hanterar meddelanden

	def on_close(self):
		router.removeConnection(self)
		print "Websocket closed."

	def check_origin(self,origin):
		return True

     # r regexp betyder att vi ska matcha
	# vilken klass ska hantera detta 
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    ])

def main():
    # pika.log.setup(color=True)
 
 	# Get a handle to the instance of ioloop
    io_loop = tornado.ioloop.IOLoop.instance()
 
    # PikaClient is our rabbitmq consumer
    pc = PikaClient(io_loop)
    pc.connect()

    router.pc = pc

    if(len(sys.argv) > 1):
         port = int(sys.argv[1])
    else:
         port = 3000
 
    application.listen(port) # listen to the port
    io_loop.start() # start the ioloop



# By doing the main check, 
# you can have that code only execute when you want to run the module as a program 
# and not have it execute when someone just wants to import your module 
# and call your functions themselves.
# For example, if the python interpreter is running that module (the source file) as the main program, 
# it sets the special __name__ variable to have a value "__main__". 
# If this file is being imported from another module, __name__ will be set to the module's name.
if __name__ == "__main__":
    main()
