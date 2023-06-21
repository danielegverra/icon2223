from ItinerarySearchProblem import ItinerarySearchProblem
from Libs.searchGeneric import Searcher, AStarSearcher

from geopy.distance import distance
import logging as log
from NodeGraph import NodeGraph
import pickle as pk
from pyswip import Prolog
import random as rd
import math

import sys

sys.path.append("Knowledge")

# Set up log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logMainSearch.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)

# Opening prolog facts file (write mode)
fileRead = open("Knowledge/Facts.pl", "r")
log.info("File opened correctly.\n")
text = fileRead.readlines()

# Opening prolog facts file (write mode)
fileWrite = open("Knowledge/RuntimeFacts.pl", "w")
log.info("File opened correctly.\n")
fileWrite.writelines(text[:17593])

print(
    "#####   Welcome to Rome Rome's treasures unveiled: an insider's journey.   #####"
)
print(
    "#####   With this software you can find the most suitable tourist route for your needs.   #####\n"
)

# Dictionary de-serialization
with open("Storage/poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")

# Assertion new facts
keys = list(poiMap.keys())
for i in range(len(keys)):
    key = keys[i]
    value = poiMap[key]
    dist = int(
        distance(
            (41.89901596243367, 12.476272269051156), (value.lat, value.lon)
        ).meters  # random coordinates
    )
    fileWrite.write(f"distance('Start','{value.name}',{dist}).\n")
fileWrite.writelines(text[17593:])
log.info("Distance facts created.\n")

# Prolog KB initialization
prolog = Prolog()
prolog.consult("Knowledge/RuntimeFacts.pl")
prolog.consult("Knowledge/Rules.pl")
log.info("Prolog consulted correctly.\n")

# Input from user
userBudget = int(input("--> Insert your budget in euro (integer): "))
userTimeAvailable = int(input("--> Insert the time in minutes available (integer): "))
log.info("Input data received correctly.\n")

# Initialize the starting node for the search
node = NodeGraph("Start", 0, userBudget, userTimeAvailable, [], 0)
log.info("Starting node initialized correctly.\n")

# Create the search problem using the initialized node and Prolog KB
problem = ItinerarySearchProblem(prolog, node)
log.info("Search problem defined correctly.\n")

# Create a base searcher to find a path
baseSearcher = Searcher(problem)
log.info("Search problem defined correctly.\n")

print("PERCORSO TROVATO CON SEARCHER BASE:")
print(baseSearcher.search())
log.info("Path found correctly.\n")

# Create an A* searcher to find a path using the problem
aStarSearcher = AStarSearcher(problem)
log.info("Search problem defined correctly.\n")

print("PERCORSO TROVATO CON SEARCHER A STAR:")
print(aStarSearcher.search())
log.info("Path found correctly.\n")

# Select a subset of visited nodes for feedback
visitedNodes = aStarSearcher.solution.end().visitedNodes[:]
visitedNodes.remove("Start")
feedbackNodes = rd.sample(visitedNodes, math.ceil(visitedNodes.__len__()*0.3))

# Open the file to store user feedback
fileFeedback = open("Storage/UserFeedback.txt", "a")

# Prompt the user for feedback on selected nodes
for node in feedbackNodes:
    print(f"What do you think about {node}?")
    userFeedback = int(input("--> Insert a number from 1 to 5: "))
    print(userFeedback)
    fileFeedback.write(f"{node},{userFeedback}\n")
