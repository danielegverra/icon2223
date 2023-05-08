import logging as log
import requests as rq
import time as tm


from Landmark import Landmark
from yelpapi import YelpAPI as yelp


def apiCall(latitude: float, longitude: float):
    api_key = "AIzaSyDLviZEMhmqbosipmU7_LMTJkFtKeeeMJA"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&type=tourist_attraction&rankby=distance&key={api_key}"
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
"""
responseWest = apiCall(centerLatitude, centerLongitude - lonOffset)
responseNorth = apiCall(centerLatitude + latOffset, centerLongitude)
responseSouth = apiCall(centerLatitude - latOffset, centerLongitude)
"""

for i in data:
    print(i["name"])
    print(i["geometry"]["location"])
    print(i["types"])
    print(i["vicinity"])
    print()
print(data.__len__())


"""
if (
    (responseEst.status_code == 200)
    & (responseWest.status_code == 200)
    & (responseNorth.status_code == 200)
    & (responseSouth.status_code == 200)
):
    log.info("Data obtained correctly.")
    
    poiMap = {}
    responseInMap(poiMap, responseEst)
    responseInMap(poiMap, responseWest)
    responseInMap(poiMap, responseNorth)
    responseInMap(poiMap, responseSouth)

    printMapLength(poiMap)
    # printMap(poiMap)

else:
    log.info("Error in obtaining data.")
"""
