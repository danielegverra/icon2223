import time
from ItinerarySearchProblem import ItinerarySearchProblem
from Libs.searchGeneric import Searcher, AStarSearcher

from geopy.distance import distance
from NodeGraph import NodeGraph
import pickle as pk
from pyswip import Prolog
import random as rd
import math

import sys

sys.path.append("Knowledge")


# Opening prolog facts file (write mode)
fileRead = open("Knowledge/Facts.pl", "r")
text = fileRead.readlines()

# Opening prolog facts file (write mode)
fileWrite = open("Knowledge/RuntimeFacts.pl", "w")
fileWrite.writelines(text[:17593])

print("\n\n#####   Welcome to Rome's treasures unveiled: an insider's journey.   #####")
print("With this software you can find the most suitable tourist route for your needs.")

# Dictionary de-serialization
with open("Storage/poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)

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

# Prolog KB initialization
prolog = Prolog()
prolog.consult("Knowledge/RuntimeFacts.pl")
prolog.consult("Knowledge/Rules.pl")

# Input from user
print()
while True:
    try:
        userBudget = int(input("\n--> Insert your budget in euro (integer): "))
        if userBudget < 1:
            raise Exception
        break
    except:
        print("\n!!! INSERT A VALID INPUT.")
while True:
    try:
        userTimeAvailable = int(
            input("\n--> Insert the time in minutes available (integer): ")
        )
        if userTimeAvailable < 1:
            raise Exception
        break
    except:
        print("\n!!! INSERT A VALID INPUT.")


# Initialize the starting node for the search
node = NodeGraph("Start", 0, userBudget, userTimeAvailable, [], 0)

# Create the search problem using the initialized node and Prolog KB
problem = ItinerarySearchProblem(prolog, node)

# Create a base searcher to find a path
baseSearcher = Searcher(problem)

print("\n\nPath found using base searcher:")
start_time = time.time()
baseSearcher.search()
if baseSearcher.solution is not None:
    print(baseSearcher.solution)
else:
    print("!!! NO SUITABLE PATH WAS FOUND FOR YOUR NEEDS.")
end_time = time.time()
execution_time = end_time - start_time
print("Execution time: ", execution_time, " seconds")

# Create an A* searcher to find a path using the problem
aStarSearcher = AStarSearcher(problem)

print("\n\nPath found using A* searcher:")
start_time = time.time()
aStarSearcher.search()
if aStarSearcher.solution is not None:
    print(aStarSearcher.solution)
else:
    print("!!! NO SUITABLE PATH WAS FOUND FOR YOUR NEEDS.")
end_time = time.time()
execution_time = end_time - start_time
print("Execution time: ", execution_time, " seconds")

# Select a subset of visited nodes for feedback
if aStarSearcher.solution is not None:
    visitedNodes = aStarSearcher.solution.end().visitedNodes[:]
    visitedNodes.remove("Start")
    feedbackNodes = rd.sample(visitedNodes, math.ceil(visitedNodes.__len__() * 0.3))

    # Open the file to store user feedback
    fileFeedback = open("Storage/UserFeedback.txt", "a")

    # Prompt the user for feedback on selected nodes
    for node in feedbackNodes:
        print(f"\n\nWhat do you think about {node}?")
        while True:
            try:
                userFeedback = int(input("--> Insert a number from 1 to 5: "))
                if userFeedback < 1 or userFeedback > 5:
                    raise Exception
                fileFeedback.write(f"{node},{userFeedback}\n")
                break
            except:
                print("\n!!! INSERT A VALID INPUT.")
