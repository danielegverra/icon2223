import logging as log
import pickle as pk
import random as rd


import sys

sys.path.append("Knowledge")


# Dictionary de-serialization
with open("Storage/poiDictionaryEnhanced.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")


# Random feedback generation
with open("Storage/UserFeedback.txt", "a") as feed:
    for poi in poiMap.values():
        ratingCount = poi.ratingCount
        name = poi.name
        for i in range(int(ratingCount * 0.4)):
            generatedRating = rd.randint(1, 5)
            feed.write(f"{name},{generatedRating}\n")
