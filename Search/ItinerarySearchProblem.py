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
        """is True if node is a goal"""
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
        return isGoal

    def neighbors(self, node):
        neighs = list(self.prolog.query(f"findNeighbors('{node.name}', Neighbors)"))[0][
            "Neighbors"
        ]
        arcs = []
        newVisitedNodes = node.visitedNodes
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
                nodeGraph = NodeGraph(
                    neigh,
                    node.coveredDistance + int(dist[0]["Distance"]),
                    node.remainingBudget - int(cost[0]["Price"]),
                    node.remainingTime - int(time[0]["TimeToVisit"]),
                    newVisitedNodes,
                )
                if nodeGraph.remainingBudget >= 0 and nodeGraph.remainingTime >= 0:
                    arcs.append(Arc(node, nodeGraph, int(dist[0]["Distance"])))
        return arcs

    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden in the hmap."""
        if node in self.hmap:
            return self.hmap[node]
        else:
            return 0

    def __repr__(self):
        """returns a string representation of the search problem"""
        res = ""
        for arc in self.arcs:
            res += str(arc) + ".  "
        return res

    def neighbor_nodes(self, node):
        """returns an iterator over the neighbors of node"""
        return (path.to_node for path in self.neighs[node])
