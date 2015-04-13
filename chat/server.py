import tornado.ioloop
import tornado.web
import tornado.websocket
import sys
import tornado.log

import router

from tornado.options import define, options

tornado.log.enable_pretty_logging()

class MainHandler(tornado.web.RequestHandler):
	def get(self):
	 	self.write("Hello world")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		router.addConnection(self) # Connect to router

		print "You are connected."

	def on_message(self,message):
		router.handleMessage(self, message)

	def on_close(self):
		router.removeConnection(self)
		print "Websocket closed."

	def check_origin(self,origin):
		print "Origin: " + origin
		return True

    # r regexp betyder att vi ska matcha
	# vilken klass ska hantera detta 
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    ])

def main():
	# Get a handle to the instance of ioloop
    io_loop = tornado.ioloop.IOLoop.instance()

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
