import json
import networkx as nx

userNode='userNode'
topicNode='topicNode'

# Create an empty graph with no nodes and no edges 
g = nx.Graph()
# Add the nodes 
g.add_node(userNode)
g.add_node(topicNode)



# Här börjar vår gamla kod 


# store connections
#clients = []
# store usernames
#users = []

# get user name
#def getUserName(socket):
#	i = clients.index(socket)

#	return users[i]

# set user name
#def setUserName(socket, newUserName):
#	newUserName = str(newUserName)
#	userName = newUserName

#	if userName == '':
#		userName = getUserName(socket)
#		if userName is None:
#			socket.write_message('You must choose a new username')
#		else:
#			socket.write_message('Your username is: ', userName)
#	else:
#		socket.write_message('Your username is: ', userName)

#	i = clients.index(socket)
#	users.append(userName)
#	socket.write_message("Your username is " + userName)

# handle message
#def handleMessage(socket, message):
	#print "Message: %s" % message
#	usrandmessage = message.partition(" ")

#	if (usrandmessage[0] == "usr"):
#		usr = usrandmessage[2]
#		setUserName(socket, usr)

	#elif (usrandmessage[0] == "exit"):
	#	removeConnection(socket)

#	else:
#		if (len(users) == 0):
#			socket.write_message("Set a username first!")
#			return

#		userName = getUserName(socket)
#		if userName is None:
#			socket.write_message("Set a username first!")
#			return

#		message = {
#			'user': userName,
#			'body': message
#		}

#		print "Send message"
#		routing_key = socket.routing_key
#		sendMessage = json.dumps(message)

		#print sendMessage
#		pc.send_message(routing_key, sendMessage)

#def processMessage(routing_key, message):
#	ind=[]
#	for socket in clients:
#		if socket.routing_key == routing_key:
#			ind.append(clients.index(socket))

#	for i in range(0,len(ind)):
#		s = clients[ind[i]] 
#		data = dict(json.loads(message))

#		s.write_message("%s says %s" % (data['user'], data['body']))

# add connection
#def addConnection(socket):
#	clients.append(socket)
#	print clients
#	socket.routing_key = 'routing_key'
g.add_node(socket)


# remove connection
#def removeConnection(socket):
#	i = clients.index(socket)
#	clients.remove(socket)
# Remove username node
	
	# Remove socket node
	g.remove_node(socket)


	#del clients[i]