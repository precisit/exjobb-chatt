import networkx as nx
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

# add user name
	def setUserName(socket):
		if userName == getUserName(socket) is not ''
			newUserName = raw_input("Enter username: ")
				if newUserName == ''
					socket.write_message('You must choose a username.')
				else
					userName = newUserName
					socket.write_message('Your username is: ' + userName)

# handle message

# add connection
	def addConnection(socket):
		clients.append(socket)
		socket.routing_key = None

# remove connection
	def removeConnection(socket):
		clients.remove(socket)

