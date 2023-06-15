from geopy.distance import distance
from pyswip import Prolog


import pickle as pk
import logging as log


# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logKbManager.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)


# Dictionary de-serialization
with open("Storage/poiDictionary.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")


# Opening prolog facts file (write mode)
file = open("Knowledge/Facts.pl", "w")
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
prolog.consult("Knowledge/Facts.pl")
prolog.consult("Knowledge/Rules.pl")
log.info("Prolog consulted correctly.\n")


# Opening prolog facts file (append mode)
file = open("Knowledge/Facts.pl", "a")
log.info("File opened correctly.\n")


# Deletion unconnected poi
unusedPoi = []
for value in poiMap.values():
    if not bool(list(prolog.query(f"connectivityCheck('{value.name}')"))):
        unusedPoi.append(value.placeId)
for poi in unusedPoi:
    del poiMap[poi]


# Creation new feature (density)
for value in poiMap.values():
    result = list(prolog.query(f"calculateDensity('{value.name}', Density)"))
    value.density = int(result[0]["Density"])
log.info("Density feature created correctly.\n")


# Creation new feature (TourismRateOutOfTen)
for value in poiMap.values():
    result = list(
        prolog.query(
            f"calculateTourismRateOutOfTen('{value.name}', TourismRateOutOfTen)"
        )
    )
    value.tourismRateOutOfTen = int(result[0]["TourismRateOutOfTen"])
    file.write(f"tourismRateOutOfTen('{value.name}',{value.tourismRateOutOfTen}).\n")
log.info("TourismRateOutOfTen feature created correctly.\n")


# Closing prolog facts file
file.close()
log.info("File closed correctly.\n")


# Reloaded facts file
prolog.consult("Knowledge/Facts.pl")
log.info("Prolog consulted correctly.\n")


# Opening prolog facts file (append mode)
file = open("Knowledge/Facts.pl", "a")
log.info("File opened correctly.\n")


# Creation new feature (highlyRated)
for value in poiMap.values():
    if bool(list(prolog.query(f"highlyRated('{value.name}')"))):
        value.highlyRated = True
    else:
        value.highlyRated = False
log.info("HighlyRated feature created correctly.\n")


# Creation new feature (popular)
for value in poiMap.values():
    if bool(list(prolog.query(f"popular('{value.name}')"))):
        value.popular = True
    else:
        value.popular = False
log.info("Popular feature created correctly.\n")


# Creation new feature (highlyRecommended)
for value in poiMap.values():
    if bool(list(prolog.query(f"highlyRecommended('{value.name}')"))):
        value.highlyRecommended = True
    else:
        value.highlyRecommended = False
log.info("highlyRecommended feature created correctly.\n")


# Creation new feature (closeToCityCentre)
for value in poiMap.values():
    if bool(list(prolog.query(f"closeToCityCentre('{value.name}')"))):
        value.closeToCityCentre = True
    else:
        value.closeToCityCentre = False
log.info("CloseToCityCentre feature created correctly.\n")


# Creation new feature (topTourismAttraction)
for value in poiMap.values():
    if bool(list(prolog.query(f"topTourismAttraction('{value.name}')"))):
        value.topTourismAttraction = True
    else:
        value.topTourismAttraction = False
log.info("TopTourismAttraction feature created correctly.\n")


# Creation new feature (ancient)
for value in poiMap.values():
    if bool(list(prolog.query(f"ancient('{value.name}')"))):
        value.ancient = True
    else:
        value.ancient = False
log.info("Ancient feature created correctly.\n")


# Creation new feature (impressive)
for value in poiMap.values():
    if bool(list(prolog.query(f"impressive('{value.name}')"))):
        value.impressive = True
    else:
        value.impressive = False
log.info("Impressive feature created correctly.\n")


# Creation new feature (cheap)
for value in poiMap.values():
    if bool(list(prolog.query(f"cheap('{value.name}')"))):
        value.cheap = True
    else:
        value.cheap = False
log.info("Cheap feature created correctly.\n")


# Creation new feature (timeToVisit)
for value in poiMap.values():
    result = list(prolog.query(f"calculateTimeToVisit('{value.name}', TimeToVisit)"))
    value.timeToVisit = result[0]["TimeToVisit"]
log.info("TimeToVisit feature created correctly.\n")


# Creation new feature (tourismPriority)
for value in poiMap.values():
    result = list(
        prolog.query(f"calculateTourismPriority('{value.name}', TourismPriority)")
    )
    value.tourismPriority = round(result[0]["TourismPriority"], 1)
log.info("TourismPriority feature created correctly.\n")


for poi in poiMap.values():
    log.info(poi)
log.info(f"Map populated correctly ({poiMap.__len__()}).\n")


# Dictionary serialization
with open("Storage/poiDictionaryEnhanced.pickle", "wb") as f:
    pk.dump(poiMap, f)
log.info("Map serialized correctly.\n")
