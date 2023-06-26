from NodeGraph import NodeGraph
from pyswip import Prolog
from Libs.searchProblem import Search_problem, Arc


import math


class ItinerarySearchProblem(Search_problem):

    """A search problem consists of:
    * a list or set of nodes
    * a list or set of arcs
    * a start node
    * a list or set of goal nodes
    * a dictionary that maps each node into its heuristic value.
    * a dictionary that maps each node into its (x,y) position
    """

    def __init__(self, prolog, start=None, goals=set(), positions={}):
        self.prolog = prolog
        self.start = start
        self.goals = goals
        self.positions = positions

    def start_node(self):
        return self.start

    # Check if a given node is goal.
    def is_goal(self, node):
        # Query the prolog knowledge base to find the neighbors of the current node
        neighs = list(self.prolog.query(f"findNeighbors('{node.name}', Neighbors)"))[0][
            "Neighbors"
        ]

        # Initialize a flag to indicate if the node is a goal node
        isGoal = True

        # Check each neighbor of the current node
        for neigh in neighs:
            if str(neigh) not in node.visitedNodes:
                cost = list(self.prolog.query(f"price('{neigh}', Price)"))
                time = list(
                    self.prolog.query(f"calculateTimeToVisit('{neigh}', TimeToVisit)")
                )
                if (
                    node.remainingBudget - int(cost[0]["Price"]) >= 0
                    and node.remainingTime - int(time[0]["TimeToVisit"]) >= 0
                ):
                    isGoal = False
        if (
            isGoal
            and not node.sumVisitedPriority / (node.visitedNodes.__len__() - 1) >= 3.7
        ):
            isGoal = False
        return isGoal

    # Finds the neighboring nodes of a given node.
    def neighbors(self, node):
        # Query the prolog knowledge base to find the neighbors of the current node
        neighs = list(self.prolog.query(f"findNeighbors('{node.name}', Neighbors)"))[0][
            "Neighbors"
        ]
        # Initialize an empty list to store the arcs
        arcs = []

        # Create a copy of the visitedNodes list and append the name of the current node
        newVisitedNodes = node.visitedNodes[:]
        newVisitedNodes.append(str(node.name))

        # Iterate over each neighbor
        for neigh in neighs:
            # Check if the neighbor is not already visited
            if str(neigh) not in node.visitedNodes:
                # Query the prolog knowledge base to find the distance, cost, time, and tourism priority of the node
                dist = list(
                    self.prolog.query(
                        f"findDistance('{node.name}', '{neigh}', Distance)"
                    )
                )
                cost = list(self.prolog.query(f"price('{neigh}', Price)"))
                time = list(
                    self.prolog.query(f"calculateTimeToVisit('{neigh}', TimeToVisit)")
                )
                visitedPriority = list(
                    self.prolog.query(
                        f"calculateTourismPriority('{neigh}', TourismPriority)"
                    )
                )
                # Create a new NodeGraph object representing the neighbor node with updated attributes
                nodeGraph = NodeGraph(
                    neigh,
                    node.coveredDistance + int(dist[0]["Distance"]),
                    node.remainingBudget - int(cost[0]["Price"]),
                    node.remainingTime - int(time[0]["TimeToVisit"]),
                    newVisitedNodes,
                    node.sumVisitedPriority
                    + int(visitedPriority[0]["TourismPriority"]),
                )
                # Check if the remaining budget and remaining time of the nodeGraph are non-negative
                if nodeGraph.remainingBudget >= 0 and nodeGraph.remainingTime >= 0:
                    # Create an Arc object from the current node to the neighbor node and add it to the arcs list
                    arcs.append(Arc(node, nodeGraph, int(dist[0]["Distance"])))
        return arcs

    # Function to calculate the heuristic value of input node
    def heuristic(self, node):
        # Check if the current node is a goal node
        if self.is_goal(node):
            return 0
        else:
            # Query the prolog knowledge base to find the minimum distance
            minDistance = int(
                list(self.prolog.query(f"findMinDistance(MinDistance)"))[0][
                    "MinDistance"
                ]
            )
            # Calculate the node's priority
            if node.name != "Start":
                nodePriority = round(
                    list(
                        self.prolog.query(
                            f"calculateTourismPriority('{node.name}', TourismPriority)"
                        )
                    )[0]["TourismPriority"],
                    1,
                )
            else:
                # If the node is the start node, set its priority to 0
                nodePriority = 0
            if node.remainingTime <= node.remainingBudget:
                maxTime = int(
                    list(self.prolog.query(f"findMaxTimeToVisit(MaxTimeToVisit)"))[0][
                        "MaxTimeToVisit"
                    ]
                )
                # Calculate the heuristic value using the remaining time, maximum time to visit, minimum distance, and node priority
                heuristicValue = math.ceil(
                    node.remainingTime
                    / maxTime
                    * minDistance
                    * (1 - 0.05 * nodePriority)
                )
            else:
                maxCost = int(
                    list(self.prolog.query(f"findMaxPrice(MaxPrice)"))[0]["MaxPrice"]
                )
                # Calculate the heuristic value using the remaining budget, maximum time to visit, minimum distance, and node priority
                heuristicValue = math.ceil(
                    node.remainingBudget
                    / maxCost
                    * minDistance
                    * (1 - 0.05 * nodePriority)
                )
            return heuristicValue

    def __repr__(self):
        """returns a string representation of the search problem"""
        res = ""
        for arc in self.arcs:
            res += str(arc) + ".  "
        return res

    def neighbor_nodes(self, node):
        """returns an iterator over the neighbors of node"""
        return (path.to_node for path in self.neighs[node])
