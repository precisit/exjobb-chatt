import json
import networkx as nx
import pika
from pika import adapters

userNode='userNode'
#topicNode='topicNode'

# Create an empty graph with no nodes and no edges 
g = nx.Graph()
# Add the nodes 
g.add_node(userNode)
#g.add_node(topicNode)

# Old code

# store connections
#clients = []
# store usernames
#users = []

# get user name
def getUserName(socket):
	#i = clients.index(socket)
	#return users[i]

	try:
		return list(nx.common_neighbors(g, socket, userNode))[0]
	except (nx.NetworkXError, IndexError):
		return None

# set user name
def setUserName(socket, newUserName):
	newUserName = str(newUserName)
	userName = newUserName

#	if userName == '':
#		userName = getUserName(socket)
#		if userName is None:
#			socket.write_message('You must choose a new username')
#		else:
#			socket.write_message('Your username is: ', userName)
#	else:
#		socket.write_message('Your username is: ', userName)

	g.add_edge(newUserName, socket)
	g.add_edge(newUserName, userNode)

	pc.bind_client_queue(newUserName)

	#i = clients.index(socket)
	#users.append(userName)
	socket.write_message("Your username is " + userName)

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
		userName = getUserName(socket)
		if userName is None:
			socket.write_message("Set a username first!")
			return

		message = {
			'user': userName,
			'body': message
		}

		print "Send message"
		routing_key = socket.routing_key
		sendMessage = json.dumps(message)

		#print sendMessage
		pc.send_client_message(routing_key, sendMessage)

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
	#clients.append(socket)
	#print clients
	socket.routing_key = 'routing_key'
	g.add_node(socket)


# remove connection
def removeConnection(socket):
	#i = clients.index(socket)
	#clients.remove(socket)
	userName = getUserName(socket)
	if userName is not None:
		g.remove_node(userName)

		pc.unbind_queue(userName)

	# Remove socket node
	g.remove_node(socket)


	#del clients[i]