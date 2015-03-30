import networkx as nx
import json

# The connection between the users and the topics are stored in connect
# One node for each user and one node for each topic and one node for each socket
# Users are accessed by getting neighbors of the userRootNode
# Topics are accessed by getting neighbors of the topicRootNode
connect=nx.Graph()
connect.add_node('userRootNode')
connect.add_node('topicRootNode')

	def addConnection(socket): 
		connect.add_node(socket)
		socket.routing_key=None

	def removeconnection(socket): 