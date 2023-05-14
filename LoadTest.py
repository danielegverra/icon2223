import pickle as pk
import logging as log
import Preprocessor as pp

# Dictionary de-serialization
with open("poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)
