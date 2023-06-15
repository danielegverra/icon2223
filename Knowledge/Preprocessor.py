from geopy.distance import distance
from Landmark import Landmark


import logging as log
import pickle as pk
import random as rd
import requests as rq
import time as tm
import unicodedata as ucd


# API call to fetch nearby tourist attractions based on latitude and longitude
def apiCall(latitude: float, longitude: float):
    api_key = "AIzaSyDLviZEMhmqbosipmU7_LMTJkFtKeeeMJA"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&type=tourist_attraction&radius=1500&key={api_key}"
    return rq.get(url)


# API call to fetch the next page of results using the page token
def apiCallNext(pagetoken: str):
    api_key = "AIzaSyDLviZEMhmqbosipmU7_LMTJkFtKeeeMJA"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={pagetoken}&key={api_key}"
    return rq.get(url)


# Extracts the results from the API response and appends them to the list
def extractResults(list: list, response: rq.Response):
    list += response.json().get("results")
    page_token = response.json().get("next_page_token")
    while page_token:
        tm.sleep(2)
        response = apiCallNext(page_token)
        list += response.json().get("results")
        page_token = response.json().get("next_page_token")
    return list


# Generates a random value between the given range
def generateRandomValue(start, end):
    if rd.random() < 0.5:
        return 0
    else:
        return rd.randint(start, end)


# Populates the map dictionary with landmarks from the list
def populateMap(map: dict, l: list):
    for i in l:
        if i["place_id"] not in map and i["user_ratings_total"] >= 15:
            poi = Landmark(
                i["place_id"],
                ucd.normalize("NFKD", i["name"])
                .encode("ASCII", "ignore")
                .decode("utf-8")
                .replace("'", " "),
                ucd.normalize("NFKD", i["vicinity"])
                .encode("ASCII", "ignore")
                .decode("utf-8")
                .replace("'", " "),
                rd.choice(
                    [
                        "Monument",
                        "Castle",
                        "Museum",
                        "Place of warship",
                        "Square",
                        "Park",
                        "Viewpoint",
                        "Bridge",
                        "Fountain",
                    ]
                ),
                generateStringList(
                    ["Historical", "Modern art", "Entertainment", "Educational"]
                ),
                i["geometry"]["location"]["lat"],
                i["geometry"]["location"]["lng"],
                i["rating"],
                i["user_ratings_total"],
                int(
                    distance(
                        (centerLatitude, centerLongitude),
                        (
                            i["geometry"]["location"]["lat"],
                            i["geometry"]["location"]["lng"],
                        ),
                    ).meters
                ),
                rd.choice([True, False]),
                rd.randint(200000, 1500000),
                rd.randint(200, 2000),
                round(rd.uniform(400, 8000), 2),
                round(rd.uniform(0, 20), 2),
                generateRandomValue(5, 12),
            )
            map[i["place_id"]] = poi
            log.info(poi)


# Generates a list of strings from the given list with random choices
def generateStringList(l: list):
    generatedList = []
    while len(set(generatedList)) == 0:
        generatedList = rd.choices(l, k=rd.randint(1, 3))
    return list(set(generatedList))


# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("Logs/logPreprocessor.txt", mode="w")
handler.setLevel(log.INFO)
log.getLogger("").addHandler(handler)


# Coordinates of the "tourist" center of Rome
centerLatitude = 41.8995134
centerLongitude = 12.4762505


# Coordinate offset 1.5km
latOffset = 0.0135
lonOffset = 0.0176


# Multiple calls due to api limitations: Est, West, North, South
data = list()
responseEst = apiCall(centerLatitude, centerLongitude + lonOffset)
data = extractResults(data, responseEst)
responseWest = apiCall(centerLatitude, centerLongitude - lonOffset)
data = extractResults(data, responseWest)
responseNorth = apiCall(centerLatitude + latOffset, centerLongitude)
data = extractResults(data, responseNorth)
responseSouth = apiCall(centerLatitude - latOffset, centerLongitude)
data = extractResults(data, responseSouth)
log.info("Api calls executed correctly.\n")


# Dictionary population
poiMap = {}
populateMap(poiMap, data)
log.info(f"Map populated correctly ({poiMap.__len__()}).\n")


# Adjustments to the main pois


# Colosseo
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].type = "Monument"
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].properties = ["Historical", "Educational"]
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].tourismRate = 6400000
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].age = 1936
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].surface = 20000
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].height = 48
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].price = 16


# Basilica San Pietro
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].type = "Place of warship"
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].properties = ["Historical", "Educational"]
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].tourismRate = 11400000
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].age = 506
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].surface = 22000
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].height = 136
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].price = 0


# Foro Romano
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].type = "Monument"
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].properties = ["Historical", "Educational"]
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].tourismRate = 4500000
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].age = 2500
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].surface = 160000
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].price = 16


# Musei Vaticani
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].type = "Museum"
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].properties = ["Historical", "Educational"]
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].tourismRate = 6700000
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].age = 500
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].surface = 420000
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].price = 17


# Fontana di Trevi
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].type = "Fountain"
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].properties = ["Historical", "Entertainment"]
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].tourismRate = 6500000
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].age = 260
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].surface = 2400
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].height = 26
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].price = 0


# Pantheon
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].type = "Museum"
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].properties = ["Historical", "Educational"]
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].tourismRate = 7400000
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].age = 2000
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].surface = 680
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].height = 43
poiMap["ChIJqUCGZ09gLxMRLM42IPpl0co"].price = 0


# Piazza Navona
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].type = "Square"
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].properties = ["Historical", "Entertainment"]
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].tourismRate = 5700000
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].age = 400
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].surface = 14000
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].height = 0
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].price = 0


# Villa Borghese
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].type = "Park"
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].properties = ["Entertainment"]
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].age = 400
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].surface = 80000
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].price = 13


# Castel San Angelo
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].type = "Castle"
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].properties = ["Historical", "Educational"]
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].tourismRate = 1300000
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].age = 1900
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].surface = 49000
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].height = 57
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].price = 15
log.info("Most important poi modified correctly.\n")


# Dictionary serialization
with open("Storage/poiDictionary.pickle", "wb") as f:
    pk.dump(poiMap, f)
log.info("Map serialized correctly.\n")
