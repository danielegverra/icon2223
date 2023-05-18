from geopy.distance import distance
from Landmark import Landmark


import logging as log
import pickle as pk
import random as rd
import requests as rq
import time as tm
import unicodedata as ucd
import Utility as ut


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


def generate_random_value(start, end):
    if rd.random() < 0.5:
        return 0
    else:
        return rd.randint(start, end)


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
                i["types"],
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
                generate_random_value(5, 12),
            )
            map[i["place_id"]] = poi
            log.info(poi)


# START APPLICATION

# Log configuration
log.basicConfig(level=log.INFO)
handler = log.FileHandler("logPreprocessor.txt", mode="w")
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

# Adjustments to the main pois

# Colosseo
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].tourismRate = 6400000
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].age = 1936
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].surface = 20000
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].height = 48
poiMap["ChIJrRMgU7ZhLxMRxAOFkC7I8Sg"].price = 16

# Basilica San Pietro
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].tourismRate = 11400000
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].age = 506
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].surface = 22000
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].height = 136
poiMap["ChIJWZsUt2FgLxMRg1KHzXfwS3I"].price = 0

# Foro Romano
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].tourismRate = 4500000
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].age = 2500
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].surface = 160000
poiMap["ChIJ782pg7NhLxMR5n3swAdAkfo"].price = 16

# Musei Vaticani
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].tourismRate = 6700000
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].age = 500
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].surface = 420000
poiMap["ChIJKcGbg2NgLxMRthZkUqDs4M8"].price = 17

# Fontana di Trevi
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].tourismRate = 6500000
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].age = 260
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].surface = 2400
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].height = 26
poiMap["ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"].price = 0

# Pantheon
poiMap["ChIJd0eH3VFgLxMR59ZuxPeRwDE"].tourismRate = 7400000
poiMap["ChIJd0eH3VFgLxMR59ZuxPeRwDE"].age = 2000
poiMap["ChIJd0eH3VFgLxMR59ZuxPeRwDE"].surface = 680
poiMap["ChIJd0eH3VFgLxMR59ZuxPeRwDE"].height = 43
poiMap["ChIJd0eH3VFgLxMR59ZuxPeRwDE"].price = 0

# Piazza Navona
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].tourismRate = 5700000
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].age = 400
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].surface = 14000
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].height = 0
poiMap["ChIJPRydwYNgLxMRSjOCLlYkV6M"].price = 0

# Villa Borghese
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].age = 400
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].surface = 80000
poiMap["ChIJj1M8HQJhLxMRRI6D_z18Pes"].price = 13

# Castel San Angelo
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].tourismRate = 1300000
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].age = 1900
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].surface = 49000
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].height = 57
poiMap["ChIJ0aTnEYeKJRMRiUF95xwRbDY"].price = 15

# Dictionary serialization
with open("poiDictionary.pickle", "wb") as f:
    pk.dump(poiMap, f)
