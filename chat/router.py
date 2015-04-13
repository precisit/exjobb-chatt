import json

from collections import defaultdict

import pikaConsumer
from pikaConsumer import PikaConsumer

# store usernames
users = dict()
# store subscriptions
socketsInRoomName = defaultdict(list)

pC = PikaConsumer()
pC.open()

# set user name
def setUserName(socket, newUserName):
	print 'Username was set', newUserName
	socket.username = newUserName
	users[newUserName] = socket

	welcomeMessage = newUserName + " joined the chat. Welcome " + newUserName + "!"

	message = {
		'user': 'Chat',
		'body': welcomeMessage
	}

	jsonM = json.dumps(message)

	pC.send_message('the_first_room', jsonM)

# handle message
def handleMessage(socket, message):
	#print "Message: %s" % message'
	# TODO: Client always send JSON as well, e.g. {command: 'setUsername', username: xxxx} OR {'command': 'sendMessage', roomName: 'the_only_room', message: 'Hello World!'}
	# TODO2: Add command "joinChannel"
	# TODO3: Add command "leaveChannel"
	message = json.loads(message)
	command = message['command']

	if (command == 'setUsername'):
		usr = message['body']
		print "setting username"
		setUserName(socket, usr)

	elif (command == 'sendMessage'):
		userName = socket.username
		if userName is None:
			socket.write_message('Error: Set a username first!')
			return

		body = message['body']
		roomName = message['room']

		if (roomName == 'default'):
			roomName = 'the_first_room' # default

		message = {
			'user': userName,
			'room name': roomName,
			'body': body
		}

		print "Send message"
		jsonMessage = json.dumps(message)

		pC.send_message(roomName, jsonMessage)

	elif (command == 'join'):
		userName = socket.username
		if userName is None:
			socket.write_message('Error: Set a username first!')
			return

		roomName = message['body']
		pC.join_talkRoom(roomName)
		socketsInRoomName[roomName].append(socket)
		socket.write_message('You have joined the chat room ' + roomName)

	elif (command == 'leave'):
		userName = socket.username
		if userName is None:
			socket.write_message('Error: Set a username first!')
			return
		roomName = message['body']
		pC.leave_talkRoom(roomName)
		socketsInRoomName[roomName].remove(socket)
		socket.write_message('You have left the chat room ' + roomName)

	else:
		socket.write_message('Invalid command')

# add connection
def addConnection(socket):
	# Temporary when we have only one room, later should be set in a join chatroom method
	socket.username = None

	socketsInRoomName['the_first_room'].append(socket)
	pC.join_talkRoom('the_first_room')

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
