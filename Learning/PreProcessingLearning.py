import pandas as pd
import logging as log
import pickle as pk


import sys

sys.path.append("Knowledge")


# Function to calculate the tourism priority of a landmark
def calculateTourismPriority(poiMap, id):
    rating = poiMap[id].rating

    if poiMap[id].ratingCount > 15000:
        popular_weight = 0.6
    else:
        popular_weight = 0

    if poiMap[id].centreDistance < 501:
        close_to_city_centre_weight = 0.3
    else:
        close_to_city_centre_weight = 0

    tourism_rate_out_of_ten = poiMap[id].tourismRateOutOfTen

    if poiMap[id].age > 800:
        ancient_weight = 0.2
    else:
        ancient_weight = 0

    if poiMap[id].surface > 7000 or poiMap[id].height > 17:
        impressive_weight = 0.3
    else:
        impressive_weight = 0

    density = poiMap[id].density

    normalized_density = (density - 1138) / (2846 - 1138)

    density_weight = 0.6 - (0.6 * normalized_density)

    tourism_priority = (
        rating / 2
        + popular_weight
        + close_to_city_centre_weight
        + tourism_rate_out_of_ten * 0.05
        + ancient_weight
        + impressive_weight
        + density_weight
    )

    return tourism_priority


# Set up log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logLearning.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)


# Dictionary de-serialization
with open("Storage/poiDictionaryFeedback.pickle", "rb") as f:
    poiMap = pk.load(f)
log.info("Map de-serialized correctly.\n")


# Feedback generation
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


# Serializing generated feedbacks
with open("Storage/UserFeedback.txt", "w") as fileDelete:
    fileDelete.truncate(0)


# Refreshing pois' tourism priority
for poi in poiMap.values():
    poi.tourismPriority = round(calculateTourismPriority(poiMap, poi.placeId), 1)
    log.info(poi)
log.info(f"Map modified correctly ({poiMap.__len__()}).\n")


# Dictionary serialization
with open("Storage/poiDictionaryFeedback.pickle", "wb") as f:
    pk.dump(poiMap, f)
log.info("Map serialized correctly.\n")


# Initializing dataframe
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


# Defining useless columns
deleteColumns = [
    "Place Id",
    "Name",
    "Address",
    "Type",
    "Properties",
    "Lat",
    "Lon",
    "Highly Rated",
    "Highly Recommended",
    "Close to City Centre",
    "Handicap Accessability",
    "Tourism Rate Out of Ten",
    "Top Tourism Attraction",
    "Popular",
    "Ancient",
    "Time to Visit",
    "Impressive",
    "Price",
    "Cheap",
]


# Dataframe creation and serialization
df = pd.DataFrame(data)
df = df.drop(columns=deleteColumns)
df.to_csv("Storage/Dataframe.csv", index=False)
