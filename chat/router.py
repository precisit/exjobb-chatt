#import networkx as nx
import json
#import customserializer

# The connection between the users and the topics are stored in connect
# One node for each user and one node for each topic and one node for each socket
# Users are accessed by getting neighbors of the userRootNode
# Topics are accessed by getting neighbors of the topicRootNode

# g=nx.Graph()
# g.add_node('userRootNode')
# g.add_node('topicRootNode')

# store connections
clients = []
# store usernames
users = []

# get user name
def getUserName(socket):
	i = clients.index(socket)

	return users[i]

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

	i = clients.index(socket)
	users.append(userName)
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
		if (len(users) == 0):
			socket.write_message("Set a username first!")
			return
			
		userName = getUserName(socket)
		print userName
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
		pc.send_message(routing_key, sendMessage)

def processMessage(routing_key, message):
	for socket in clients:
		if socket.routing_key == routing_key:
			ind = clients.index(socket)

	s = clients[ind] 
	data = dict(json.loads(message))

	s.write_message("%s says %s" % (data['user'], data['body']))

# add connection
def addConnection(socket):
	clients.append(socket)
	socket.routing_key = 'routing_key'

# remove connection
def removeConnection(socket):
	i = clients.index(socket)
	clients.remove(socket)

	#del clients[i]