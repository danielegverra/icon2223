import pickle as pk
import networkx as nx
import logging as log
import sys
import math

from pyswip import Prolog

# Function to query the knowledge base and obtain the distance between two nodes
def query_prolog_distance(attraction1, attraction2):
    distance = list(prolog.query(
        f"findDistance('{attraction1}', '{attraction2}', Distance)"))
    return distance[0]['Distance']

# Function to calculate the heuristic value using a weighted sum of remaining time and cost
def calculate_heuristic(node, remaining_time, remaining_cost):
    time_to_visit = graph.nodes[node]['timeToVisit']
    price = graph.nodes[node]['price']
    return (remaining_time * time_to_visit) + (remaining_cost * price)

# Function to perform branch and bound search
def branch_and_bound(graph, start_node, max_time, max_cost):
    num_nodes = len(graph)
    best_path = []  # Miglior percorso trovato
    best_cost = math.inf  # Costo del miglior percorso trovato

    # Funzione di calcolo del limite superiore (bound) per un nodo
    def calculate_bound(path, cost, time):
        bound = 0
        last_node = path[-1]

        remaining_nodes = set(graph.nodes()) - set(path)
        remaining_time = max_time - time
        remaining_cost = max_cost - cost

        for node in remaining_nodes:
            time_to_visit = graph.nodes[node]['timeToVisit']
            price = graph.nodes[node]['price']
            distance = query_prolog_distance(last_node, node)
            if distance <= 500 and time + time_to_visit <= max_time and cost + price <= max_cost:
                bound += distance

        return bound

    # Funzione ricorsiva per l'esplorazione dei nodi
    def explore_node(path, cost, time):
        nonlocal best_path, best_cost

        if len(path) == num_nodes:
            # Arrivati a un percorso completo
            if cost < best_cost:
                best_path = path[:]
                best_cost = cost
        else:
            # Altrimenti, esplora i nodi successivi
            last_node = path[-1]
            remaining_nodes = set(graph.nodes()) - set(path)

            for node in remaining_nodes:
                distance = query_prolog_distance(last_node, node)
                time_to_visit = graph.nodes[node]['timeToVisit']
                price = graph.nodes[node]['price']
                new_path = path + [node]
                new_cost = cost + distance
                new_time = time + time_to_visit
                bound = calculate_bound(new_path, new_cost, new_time)

                if bound < best_cost:
                    explore_node(new_path, new_cost, new_time)

    # Inizia l'esplorazione dal nodo iniziale
    explore_node([start_node], 0, 0)

    return best_path, best_cost

# Main code
# Set up log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("logGraph.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)

# Load the graph from the serialized file
with open('graph.pickle', 'rb') as file:
    graph = pk.load(file)

log.info("Graph deserialized correctly.\n")

# Load the Prolog knowledge base
prolog = Prolog()
prolog.consult('Facts.pl')
prolog.consult('Rules.pl')

# Set the start node and maximum time/cost constraints
start_node = "Colosseum"
max_time = 8  # Maximum time in hours
max_cost = 50  # Maximum cost in euros

# Find the best path using branch and bound algorithm
best_path, best_cost = branch_and_bound(graph, start_node, max_time, max_cost)

if best_path:
    log.info("Best path found:")
    for node in best_path:
        log.info(node)
    log.info("Total cost: " + str(best_cost))
else:
    log.info("No feasible path found within the given constraints.")
