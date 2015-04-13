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
	#print "Message: %s" % message'
	# TODO: Client always send JSON as well, e.g. {command: 'setUsername', username: xxxx} OR {'command': 'sendMessage', roomName: 'the_only_room', message: 'Hello World!'}
	# TODO2: Add command "joinChannel"
	# TODO3: Add command "leaveChannel"
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






