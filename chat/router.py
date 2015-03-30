import networkx as nx
import json

# The connection betweem the users and the topics are stored in g
# One node for each user and one node for each topic and one node for each socket
# Users are accessed by getting neighbors of the userRootNode
# Topics are accessed by getting neighbors of the topicRootNode

g=nx.Graph()
g.add_node('userRootNode')
g.add_node('topicRootNode')

