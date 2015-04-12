import json

from collections import defaultdict

import pika
from pika import adapters
import uuid

userNode='userNode'

#topicNode='topicNode'

# Create an empty graph with no nodes and no edges 
#g = nx.Graph()
# Add the nodes 
#g.add_node(userNode)
#g.add_node(topicNode)

# store usernames
users = dict()
# store subscriptions
socketsInRoomName = defaultdict(list)

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

	def on_message(self, channel_unused, basic_deliver, properties, body):
		roomName = basic_deliver.routing_key.split('.')[1]
		print 'Message received FROM RabbitMQ on room', roomName

		for socket in socketsInRoomName[roomName]:
			socket.write_message(body)

		self.channel.basic_ack(basic_deliver.delivery_tag)

	def join_talkRoom(self, roomName):
		print 'Will join talkRoom', roomName
		if roomName not in self.roomNameSubscriptions:
			print '  - Doing new Subscribe (first)'
			self.roomNameSubscriptions[roomName] = self.channel.queue_bind(self.on_bindok, self.QUEUE, self.EXCHANGE, 'channel.' + roomName)
		else: 
			print '  - Already subscribed'

	def send_message(self, roomName, message):
		print 'Will send message to room', roomName
		self.channel.basic_publish(self.EXCHANGE, 'channel.'+roomName, message, properties=None, mandatory=False, immediate=False)

pikaConsumer = PikaConsumer()
pikaConsumer.open()


# set user name
def setUserName(socket, newUserName):
	print 'Username was set', newUserName
	socket.username = newUserName
	users[newUserName] = socket

	#users['siri'].write_message('hej')

# handle message
def handleMessage(socket, message):
	#print "Message: %s" % message
	usrandmessage = message.partition(" ")

	if (usrandmessage[0] == "usr"):
		usr = usrandmessage[2]
		setUserName(socket, usr)

	#elif (usrandmessage[0] == "exit"):
	#	removeConnection(socket)

	else:
		userName = socket.username
		if userName is None:
			socket.write_message("Set a username first!")
			return

		message = {
			'user': userName,
			'body': message
		}

		print "Send message"
		jsonMessage = json.dumps(message)

		pikaConsumer.send_message('the_only_room', jsonMessage)

		#print sendMessage
		#pc.send_client_message(message.routing_key, jsonMessage)

def processClientMessage(routing_key, message):
	#ind=[]
	#for socket in clients:
	#	if socket.routing_key == routing_key:
	#		ind.append(clients.index(socket))

	print message

	try: 
		iterator = g.neighbors_iter(routing_key)
	except nx.NetworkXError:
		print 'Invalid routing key'
		return

	data = dict(json.loads(message))

	for x in iterator:
		if x is not userNode:
			s.write_message("%s says %s" % (data['user'], data['body']))

def processServerMessage(routing_key, message):
	data = dict(json.loads(message))
	print "Server message"

# add connection
def addConnection(socket):

	# Temporary when we have only one room, later should be set in a join chatroom method
	pikaConsumer.join_talkRoom('the_only_room')
	socketsInRoomName['the_only_room'].append(socket)


	#print clients
	#socket.routing_key = 'routing_key'
	#g.add_node(socket)


# remove connection
def removeConnection(socket):
	# Remove user from dictionaries
	del users[socket.username]

	for roomName in socketsInRoomName: 
		room = socketsInRoomName[roomName]
		del room[room.index(socket)]






