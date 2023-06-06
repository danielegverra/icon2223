import math
from NodeGraph import NodeGraph
from pyswip import Prolog
from Libs.searchProblem import Search_problem, Arc


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
        """returns start node"""
        return self.start

    def is_goal(self, node):
        neighs = list(self.prolog.query(f"findNeighbors('{node.name}', Neighbors)"))[0][
            "Neighbors"
        ]
        isGoal = True
        for neigh in neighs:
            if str(neigh) not in node.visitedNodes:
                dist = list(
                    self.prolog.query(
                        f"findDistance('{node.name}', '{neigh}', Distance)"
                    )
                )
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
            and not node.sumVisitedPriority / (node.visitedNodes.__len__() - 1) >= 4
        ):
            isGoal = False
        return isGoal

    def neighbors(self, node):
        neighs = list(self.prolog.query(f"findNeighbors('{node.name}', Neighbors)"))[0][
            "Neighbors"
        ]
        arcs = []
        newVisitedNodes = node.visitedNodes[:]
        newVisitedNodes.append(str(node.name))
        for neigh in neighs:
            if str(neigh) not in node.visitedNodes:
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
                nodeGraph = NodeGraph(
                    neigh,
                    node.coveredDistance + int(dist[0]["Distance"]),
                    node.remainingBudget - int(cost[0]["Price"]),
                    node.remainingTime - int(time[0]["TimeToVisit"]),
                    newVisitedNodes,
                    node.sumVisitedPriority
                    + int(visitedPriority[0]["TourismPriority"]),
                )
                if nodeGraph.remainingBudget >= 0 and nodeGraph.remainingTime >= 0:
                    arcs.append(Arc(node, nodeGraph, int(dist[0]["Distance"])))
        return arcs

    def heuristic(self, node):
        if self.is_goal(node):
            return 0
        else:
            minDistance = int(
                list(self.prolog.query(f"findMinDistance(MinDistance)"))[0][
                    "MinDistance"
                ]
            )
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
                nodePriority = 0
            if node.remainingTime <= node.remainingBudget:
                maxTime = int(
                    list(self.prolog.query(f"findMaxTimeToVisit(MaxTimeToVisit)"))[0][
                        "MaxTimeToVisit"
                    ]
                )
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
                heuristicValue = math.ceil(
                    node.remainingTime
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
