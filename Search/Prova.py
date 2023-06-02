from ItinerarySearchProblem import ItinerarySearchProblem
from Libs.searchGeneric import Searcher

from NodeGraph import NodeGraph
from pyswip import Prolog

import sys
sys.path.append("Knowledge")

# Prolog KB initialization
prolog = Prolog()
prolog.consult('Knowledge/Facts.pl')
prolog.consult('Knowledge/Rules.pl')

node = NodeGraph("Trevi Fountain", 0, 100, 100, ["Colosseum", "Bailica"])

problem = ItinerarySearchProblem(
    prolog,
    node, 
)
searcher = Searcher(problem)
searcher.search()