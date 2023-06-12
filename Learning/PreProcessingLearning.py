import pandas as pd
import logging as log
import pickle as pk
import sys

sys.path.append("Knowledge")

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
placeId = {}

for key, value in poiMap.items():
    placeId[value.name] = key

userFeedback = []
with open("Storage/UserFeedback.txt", "r") as feed:
    for line in feed:
        line = line.strip()
        userFeedback.append(line)

for feedback in userFeedback:
    elements = feedback.split(",")
    name = elements[0]
    rating = float(elements[1])

    id = placeId[name]

    poiRating = poiMap[id].rating
    poiRatingCount = poiMap[id].ratingCount

    newAvg = poiRating + (rating - poiRating) / (poiRatingCount + 1)

    poiMap[id].rating = newAvg
    poiMap[id].ratingCount += 1

with open("Storage/UserFeedback.txt", "w") as fileDelete:
    fileDelete.truncate(0)

for poi in poiMap.values():
    log.info(poi)
log.info(f"Map modified correctly ({poiMap.__len__()}).\n")

# Dictionary serialization
with open("Storage/poiDictionaryFeedback.pickle", "wb") as f:
    pk.dump(poiMap, f)
log.info("Map serialized correctly.\n")

placeIdList = []
nameList = []
addressList = []
typeList = []
propertiesList = []
latList = []
lonList = []
ratingList = []
highlyRatedList = []
ratingCountList = []
popularList = []
highlyRecommendedList = []
centreDistanceList = []
closeToCityCentreList = []
handicapAccessibilityList = []
tourismRateList = []
tourismRateOutOfTenList = []
topTourismAttractionList = []
ageList = []
ancientList = []
surfaceList = []
heightList = []
impressiveList = []
priceList = []
cheapList = []
densityList = []
timeToVisitList = []
tourismPriorityList = []

# Learning start
for value in poiMap.values():
    placeIdList.append(value.placeId)
    nameList.append(value.name)
    addressList.append(value.address)
    typeList.append(value.type)
    propertiesList.append(value.properties)
    latList.append(value.lat)
    lonList.append(value.lon)
    ratingList.append(value.rating)
    highlyRatedList.append(value.highlyRated)
    ratingCountList.append(value.ratingCount)
    popularList.append(value.popular)
    highlyRecommendedList.append(value.highlyRecommended)
    centreDistanceList.append(value.centreDistance)
    closeToCityCentreList.append(value.closeToCityCentre)
    handicapAccessibilityList.append(value.handicapAccessibility)
    tourismRateList.append(value.tourismRate)
    tourismRateOutOfTenList.append(value.tourismRateOutOfTen)
    topTourismAttractionList.append(value.topTourismAttraction)
    ageList.append(value.age)
    ancientList.append(value.ancient)
    surfaceList.append(value.surface)
    heightList.append(value.height)
    impressiveList.append(value.impressive)
    priceList.append(value.price)
    cheapList.append(value.cheap)
    densityList.append(value.density)
    timeToVisitList.append(value.timeToVisit)
    tourismPriorityList.append(value.tourismPriority)

data = {
    "Place Id": placeIdList,
    "Name": nameList,
    "Address": addressList,
    "Type": typeList,
    "Properties": propertiesList,
    "Lat": latList,
    "Lon": lonList,
    "Rating": ratingList,
    "Highly Rated": highlyRatedList,
    "Rating Count": ratingCountList,
    "Popular": popularList,
    "Highly Recommended": highlyRecommendedList,
    "Centre Distance": centreDistanceList,
    "Close to City Centre": closeToCityCentreList,
    "Handicap Accessability": handicapAccessibilityList,
    "Tourism Rate": tourismRateList,
    "Tourism Rate Out of Ten": tourismRateOutOfTenList,
    "Top Tourism Attraction": topTourismAttractionList,
    "Age": ageList,
    "Ancient": ancientList,
    "Surface": surfaceList,
    "Height": heightList,
    "Impressive": impressiveList,
    "Price": priceList,
    "Cheap": cheapList,
    "Density": densityList,
    "Time to Visit": timeToVisitList,
    "Tourism Priority": tourismPriorityList,
}

deleteColumns = [
    "Place Id",
    "Name",
    "Address",
    "Properties",
    "Lat",
    "Lon",
    "Highly Rated",
    "Popular",
    "Highly Recommended",
    "Close to City Centre",
    "Tourism Rate Out of Ten",
    "Top Tourism Attraction",
    "Ancient",
    "Cheap",
    "Tourism Priority",
]

# Dataframe creation
df = pd.DataFrame(data)

df = df.drop(columns=deleteColumns)

df.to_csv("Storage/Dataframe.csv")
