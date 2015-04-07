#import networkx as nx
import json

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
	return clients.get(socket)

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
def handleMessage(socket, routing_key, message):
	message = {
	'user': userName,
	'body': data
	}

	pc.send_user_message(routing_key, message)

# add connection
def addConnection(socket):
	clients.append(socket)
	socket.routing_key = None

# remove connection
def removeConnection(socket):
	clients.remove(socket)

