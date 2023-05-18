from geopy.distance import distance
from pyswip import Prolog


import pickle as pk
import logging as log


# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("logKbManager.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)


# Dictionary de-serialization
with open("poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map loaded correctly.")

# Opening prolog facts file
file = open("facts.pl", "w")

# Writing facts to prolog file
for value in poiMap.values():
    file.write(f"place_id('{value.placeId}','{value.name}').\n")
for value in poiMap.values():
    file.write(f"address('{value.name}','{value.address}').\n")
# prop
for value in poiMap.values():
    file.write(f"coordinates('{value.name}','{value.lat}','{value.lon}').\n")
for value in poiMap.values():
    file.write(f"rating('{value.name}','{value.rating}').\n")
for value in poiMap.values():
    file.write(f"ratingCount('{value.name}','{value.ratingCount}').\n")
for value in poiMap.values():
    file.write(f"centreDistance('{value.name}','{value.centreDistance}').\n")
for value in poiMap.values():
    if value.handicapAccessibility:
        file.write(f"handicapAccessibility('{value.name}').\n")
for value in poiMap.values():
    file.write(f"tourismRate('{value.name}','{value.tourismRate}').\n")
for value in poiMap.values():
    file.write(f"age('{value.name}','{value.age}').\n")
for value in poiMap.values():
    file.write(f"surface('{value.name}','{value.surface}').\n")
for value in poiMap.values():
    file.write(f"height('{value.name}','{value.height}').\n")
for value in poiMap.values():
    file.write(f"price('{value.name}','{value.price}').\n")

# Creation new features
keys = list(poiMap.keys())
for i in range(len(keys)):
    key1 = keys[i]
    value1 = poiMap[key1]
    for j in range(i + 1, len(keys)):
        key2 = keys[j]
        value2 = poiMap[key2]
        dist = int(distance((value1.lat, value1.lon), (value2.lat, value2.lon)).meters)
        file.write(f"distance('{value1.name}','{value2.name}','{dist}').\n")

# Closing prolog facts file
file.close()

# Reading prolog file
prolog = Prolog()
prolog.consult("Facts.pl")
prolog.consult("Rules.pl")

# Query examples
print(
    bool(list(prolog.query("place_id('ChIJM2qBt7RhLxMRBvo4dDqpXpw','Basilica Julia')")))
)

"""
result = list(prolog.query("calculate_density('Il Tempio dei Dioscuri', Density)"))
density = result[0]["Density"]
print(f"The density is: {density}")
"""
# Dictionary serialization
