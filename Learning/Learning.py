from pyswip import Prolog

import logging as log
import pickle as pk
import sys

sys.path.append("Knowledge")

prolog = Prolog()
prolog.consult("Knowledge/RuntimeFacts.pl")

# Set up log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logLearning.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)

# Dictionary de-serialization
with open("Storage/poiDictionaryFeedback.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")

# Mettere il dizionario con il placeId nel caso

userFeedback = []
with open("Storage/UserFeedback.txt", "r") as feed:
    for line in feed:
        line = line.strip()
        userFeedback.append(line)

for feedback in userFeedback:
    elements = feedback.split(",")
    name = elements[0]
    rating = float(elements[1])

    result = list(
        prolog.query(f"place_id(Id, '{name}')")
    )
    id = result[0]["Id"]

    poiRating = poiMap[id].rating
    poiRatingCount = poiMap[id].ratingCount

    newAvg = poiRating + (rating - poiRating) / (poiRatingCount + 1)

    poiMap[id].rating = newAvg
    poiMap[id].ratingCount += 1
    print(poiMap[id])

with open("Storage/UserFeedback.txt", 'w') as fileDelete:
    fileDelete.truncate(0)
print(userFeedback)

# Dictionary serialization
with open("Storage/poiDictionaryFeedback.pickle", "wb") as f:
    pk.dump(poiMap, f)
log.info("Map serialized correctly.\n")