import logging as log
import networkx as nx
import pickle as pk
import sys

from pyswip import Prolog


sys.path.append("Knowledge")


# Function to query the knowledge base and obtain the distance between two nodes
def query_prolog_distance(attraction1, attraction2):
    distance = list(prolog.query(
        f"findDistance('{attraction1}', '{attraction2}', Distance)"))
    return distance[0]['Distance']


# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logGraphInitializer.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)

# Dictionary de-serialization
with open("Storage/poiDictionaryEnhanced.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")

# Prolog KB initialization
prolog = Prolog()
prolog.consult('Knowledge/Facts.pl')
prolog.consult('Knowledge/Rules.pl')

# Graph construction
graph = nx.Graph()
for value in poiMap.values():
    graph.add_node(value.name, price=value.price,
                   timeToVisit=value.timeToVisit, tourismPriority=value.tourismPriority)

for node1 in graph.nodes():
    for node2 in graph.nodes():
        if node1 != node2:
            distance = query_prolog_distance(node1, node2)
            if distance <= 500:
                graph.add_edge(node1, node2, weight=distance)

# Print the nodes and edges of the graph

for node in graph.nodes:
    log.info(node)

log.info("\nAll nodes have been correctly added.\n")

for u, v, attr in graph.edges(data=True):
    weight = attr['weight']
    log.info(f"Edge: {u} - {v}, Weight: {weight}")

log.info("\nAll edges have been correctly added.\n")


def check_node_connectivity(graph):
    disconnected_nodes = []

    for node in graph.nodes():
        if not any(graph.neighbors(node)):
            print(node)
            disconnected_nodes.append(node)
    if disconnected_nodes.__len__() != 0:
        print("Nodes without connections:")
        for node in disconnected_nodes:
            print(node)
    else:
        print("All nodes have at least one connection.")


# Example usage
# Assuming you have a graph called 'graph'
check_node_connectivity(graph)

# Serialize the graph to a file
with open('Storage/basicGraph.pickle', 'wb') as file:
    pk.dump(graph, file)
