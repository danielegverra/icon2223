import pickle as pk
import Preprocessor as pp

# Dictionary de-serialization
with open("poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)

pp.printMap(poiMap)
pp.printMapLength(poiMap)
