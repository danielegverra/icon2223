from geopy.distance import distance
from pyswip import Prolog

import pickle as pk
import logging as log


def calculateTourismRateOutOfTen(tourismRate):
    if tourismRate > 1500000:
        tourismRateOutOfTen = 10
    else:
        tourismRateOutOfTen = (tourismRate - 200000) / 133333.3333
        tourismRateOutOfTen = min(max(int(tourismRateOutOfTen), 1), 9)
    return tourismRateOutOfTen


# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("logKbManager.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)


# Dictionary de-serialization
with open("poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map loaded correctly.\n")

# Opening prolog facts file (write mode)
file = open("facts.pl", "w")
log.info("File opened correctly.\n")

# Writing facts to prolog file
for value in poiMap.values():
    file.write(f"place_id('{value.placeId}','{value.name}').\n")
for value in poiMap.values():
    file.write(f"address('{value.name}','{value.address}').\n")
for value in poiMap.values():
    file.write(f"type('{value.name}','{value.type}').\n")
for value in poiMap.values():
    file.write(f"properties('{value.name}',{value.properties}).\n")
for value in poiMap.values():
    file.write(f"coordinates('{value.name}',{value.lat},{value.lon}).\n")
for value in poiMap.values():
    file.write(f"rating('{value.name}',{value.rating}).\n")
for value in poiMap.values():
    file.write(f"ratingCount('{value.name}',{value.ratingCount}).\n")
for value in poiMap.values():
    file.write(f"centreDistance('{value.name}',{value.centreDistance}).\n")
for value in poiMap.values():
    if value.handicapAccessibility:
        file.write(f"handicapAccessibility('{value.name}').\n")
for value in poiMap.values():
    file.write(f"tourismRate('{value.name}',{value.tourismRate}).\n")
for value in poiMap.values():
    file.write(f"age('{value.name}',{value.age}).\n")
for value in poiMap.values():
    file.write(f"surface('{value.name}',{value.surface}).\n")
for value in poiMap.values():
    file.write(f"height('{value.name}',{value.height}).\n")
for value in poiMap.values():
    file.write(f"price('{value.name}',{value.price}).\n")
log.info("Facts written.\n")

# Creation new facts
keys = list(poiMap.keys())
for i in range(len(keys)):
    key1 = keys[i]
    value1 = poiMap[key1]
    for j in range(i + 1, len(keys)):
        key2 = keys[j]
        value2 = poiMap[key2]
        dist = int(distance((value1.lat, value1.lon), (value2.lat, value2.lon)).meters)
        file.write(f"distance('{value1.name}','{value2.name}',{dist}).\n")
log.info("Distance facts created.\n")

# Closing prolog facts file
file.close()
log.info("File closed correctly.\n")

# Reading prolog file
prolog = Prolog()
prolog.consult("Facts.pl")
prolog.consult("Rules.pl")
log.info("Prolog consulted correctly.\n")

# Opening prolog facts file (append mode)
file = open("facts.pl", "a")
log.info("File opened correctly.\n")

# Creation new feature (density)
for value in poiMap.values():
    result = list(prolog.query(f"calculateDensity('{value.name}', Density)"))
    value.density = int(result[0]["Density"])
    file.write(f"density('{value.name}',{value.density}).\n")
log.info("Density feature created correctly.\n")

# Creation new feature (TourismRateOutOfTen)
for value in poiMap.values():
    value.tourismRateOutOfTen = calculateTourismRateOutOfTen(value.tourismRate)
    file.write(f"tourismRateOutOfTen('{value.name}',{value.tourismRateOutOfTen}).\n")
log.info("TourismRateOutOfTen feature created correctly.\n")

# Closing prolog facts file
file.close()
log.info("File closed correctly.\n")

# Dictionary serialization
