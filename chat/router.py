#import networkx as nx
import json
import customserializer

# The connection between the users and the topics are stored in connect
# One node for each user and one node for each topic and one node for each socket
# Users are accessed by getting neighbors of the userRootNode
# Topics are accessed by getting neighbors of the topicRootNode

# g=nx.Graph()
# g.add_node('userRootNode')
# g.add_node('topicRootNode')

# store connections
clients = []

# get user name
def getUserName(socket):
	i = clients.index(socket)

	return clients[i]

# set user name
def setUserName(socket, newUserName):
	if newUserName == '':
		userName = getUserName(socket)
		if userName is None:
			socket.write_message('You must choode a new username')
		else:
			socket.write_message('Your username is: ', userName)
	else:
		socket.write_message('Your username is: ', userName)	

# handle message
def handleMessage(socket, message):
	print "Message: %s" % message
	userName = getUserName(socket)
	if userName is None:
		socket.write_message("Set a username first!")
		return

	message = {
	#	'user': userName,
		'body': message
	}

	print "Send message"
	routing_key = socket.routing_key
	sendMessage = json.dumps(message)

	#print sendMessage
	pc.send_message(routing_key, sendMessage)

def processMessage(routing_key, message):
	for socket in clients:
		if socket.routing_key == routing_key:
			ind = clients.index(socket)

	s = clients[ind] 
	data = dict(json.loads(message))

	s.write_message(data['body'])

# add connection
def addConnection(socket):
	clients.append(socket)
	socket.routing_key = 'routing_key'

# remove connection
def removeConnection(socket):
	clients.remove(socket)

