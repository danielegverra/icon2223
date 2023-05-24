import pickle as pk
import networkx as nx
import logging as log


from pyswip import Prolog


# Function to query the knowledge base and obtain the distance between two nodes
def query_prolog_distance(attraction1, attraction2):
    distance = list(prolog.query(
        f"findDistance('{attraction1}', '{attraction2}', Distance)"))
    return distance[0]['Distance']


# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("logGraph.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)

# Dictionary de-serialization
with open("poiDictionaryEnhanced.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")

# Prolog KB initialization
prolog = Prolog()
prolog.consult('Facts.pl')
prolog.consult('Rules.pl')

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

connected = nx.is_connected(graph)
num_nodes = graph.number_of_nodes()

if connected and num_nodes > 1:
    print("Tutti i nodi sono collegati ad almeno un altro nodo.")
else:
    print("Alcuni nodi non sono collegati ad altri nodi.")

print(poiMap.__len__())