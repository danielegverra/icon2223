import logging as log
import pickle as pk
import requests as rq
import time as tm


from Landmark import Landmark
from yelpapi import YelpAPI as yelp


def apiCall(latitude: float, longitude: float):
    api_key = "AIzaSyDLviZEMhmqbosipmU7_LMTJkFtKeeeMJA"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&type=tourist_attraction&radius=1500&key={api_key}"
    return rq.get(url)


def apiCallNext(pagetoken: str):
    api_key = "AIzaSyDLviZEMhmqbosipmU7_LMTJkFtKeeeMJA"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={pagetoken}&key={api_key}"
    return rq.get(url)


def extractResults(list: list, response: rq.Response):
    list += response.json().get("results")
    page_token = response.json().get("next_page_token")
    while page_token:
        tm.sleep(2)
        response = apiCallNext(page_token)
        list += response.json().get("results")
        page_token = response.json().get("next_page_token")
    return list


def populateMap(map: dict, l: list):
    for i in l:
        if i["place_id"] not in map:
            poi = Landmark(
                i["name"],
                i["types"],
                i["geometry"]["location"]["lat"],
                i["geometry"]["location"]["lng"],
                i["rating"],
                i["user_ratings_total"],
            )
            map[i["place_id"]] = poi


def printMap(map: dict):
    for key, value in map.items():
        print()
        print(key)
        print(value)
        print()


def printMapLength(map: dict):
    print(map.__len__())


# START APPLICATION

# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("log.txt", mode="w")
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

# Dictionary population
poiMap = {}
populateMap(poiMap, data)
printMapLength(poiMap)

# Dictionary serialization
with open("poiDictionary.pickle", "wb") as f:
    pk.dump(poiMap, f)
