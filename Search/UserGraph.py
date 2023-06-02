from geopy.distance import distance

from pyswip import Prolog

import logging as log
import networkx as nx
import pickle as pk
import sys

sys.path.append("Knowledge")

# Prolog KB initialization
prolog = Prolog()
prolog.consult('Knowledge/Facts.pl')
prolog.consult('Knowledge/Rules.pl')

# Set up log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logUserGraph.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)

# Load the graph from the serialized file
with open('Storage/basicGraph.pickle', 'rb') as file:
    graph = pk.load(file)

userName = input("Inserisci il tuo nome: ")
#position = input("Inserisci la tua posizione: ")
userLat = 41.883510
userLon = 12.488000

graph.add_node(userName)

  

'''for node in graph.nodes():
    if node(userName) != node:
        # PRENDI LE COORDINATE DALLA BASE DI CONOSENZA coordinates('Colosseum', X, Y).
        distance = int(distance((userLat, userLon), (node.lat, value2.lon)).meters)
        if distance <= 500:
            graph.add_edge(node1, node2, weight=distance)
'''