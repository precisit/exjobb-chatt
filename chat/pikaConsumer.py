import pika
from pika import adapters
import uuid
import router
import logging
import json

from pika.adapters.tornado_connection import TornadoConnection

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger('pika')
logger.setLevel(logging.WARN)
logger.addHandler(NullHandler())

class PikaConsumer(object):

	# Set up PikaClient
	cred = pika.PlainCredentials('guest', 'guest')
	param = pika.ConnectionParameters(
		host='localhost',
		virtual_host='/',
		connection_attempts=10,
		credentials=cred
	)

	QUEUE = str(uuid.uuid4())
	EXCHANGE = 'siriokerstin'

	roomNameSubscriptions = dict()

	def open(self): 
		self.connection = adapters.TornadoConnection(self.param, self.on_connection_open)

	def on_connection_open(self, connection_unused): 
		print 'Connection opened'
		self.connection.channel(on_open_callback=self.on_channel_open)

	def on_channel_open(self, channel):
		print 'Channel opened'
		self.channel = channel
		self.channel.exchange_declare(self.on_exchange_declareok, self.EXCHANGE, 'topic')

	def on_exchange_declareok(self, frame_unused):
		print 'Exchange declared ok'
		print 'Will declare queue', self.QUEUE
		self.channel.queue_declare(self.on_queue_declareok, self.QUEUE)

	def on_queue_declareok(self, method_frame):
		print 'Queue declared ok'
		print 'Will bind to routing keys as users subscribe to channels'

	def on_bindok(self, frame_unused):
		print 'Bind OK for routing key'
		self.channel.basic_consume(self.on_message, self.QUEUE)

	def on_message(self, channel_unused, basic_deliver, properties, message):
		print "New message"

		message = json.loads(message)

		roomName = basic_deliver.routing_key.split('.')[1]
		print 'Message received FROM RabbitMQ on room', roomName

		for socket in router.socketsInRoomName[roomName]:
			socket.write_message(message['user'] + " says: " + message['body'])

		self.channel.basic_ack(basic_deliver.delivery_tag)

	def join_talkRoom(self, roomName):
		print 'Will join talkRoom', roomName
		if roomName not in self.roomNameSubscriptions:
			print '  - Doing new Subscribe (first)'
			self.roomNameSubscriptions[roomName] = self.channel.queue_bind(self.on_bindok, self.QUEUE, self.EXCHANGE, 'channel.' + roomName)
		else: 
			print '  - Already subscribed'

		if roomName is not 'the_first_room':
			for socket in router.socketsInRoomName[roomName]:
				socket.write_message(socket.username + " joined the room " + roomName)

	def leave_talkRoom(self, roomName):
		if roomName not in self.roomNameSubscriptions:
			socket.write_message("You are not subscribed to this room")
		else: 
			del self.roomNameSubscriptions[roomName]

			for socket in router.socketsInRoomName[roomName]:
				socket.write_message(socket.username + " left the room " + roomName)

	def send_message(self, roomName, message):
		print 'Will send message to room', roomName
		self.channel.basic_publish(self.EXCHANGE, 'channel.'+roomName, message, properties=None, mandatory=False, immediate=False)

	def on_cancelok(self, frame_unused):
		self.channel.close() 
		print 'Closing the channel'		

	def stop_consuming(self):
	    if self.channel:
	    	self.channel.basic_cancel(self.on_cancelok, self.channel.basic_consume(self.on_message,
                                                         self.QUEUE)







