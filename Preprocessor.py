import requests as rq

from Landmark import Landmark


def apiCall(latitude: float, longitude: float):
    return rq.get(
        f"https://api.opentripmap.com/0.1/en/places/radius?radius=1500&lon={longitude}&lat={latitude}&rate=3&format=json&limit=1000&apikey=5ae2e3f221c38a28845f05b6c4fa232e8d7430baddba0e7f4d0e6941"
    )


def responseInMap(map: dict, resp: rq.Response):
    data = resp.json()
    for element in data:
        poi = Landmark(
            element["name"],
            None,
            element["wikidata"],
            element["kinds"],
            element["point"]["lat"],
            element["point"]["lon"],
        )
        poiMap[poi.refWiki] = poi


def printMap(map: dict):
    for key, value in map.items():
        print()
        print(key)
        print(value)
        print()


def printMapLength(map: dict):
    print(poiMap.__len__())


# Coordinates of the "tourist" center of Rome
centerLatitude = 41.8995134
centerLongitude = 12.4762505

# Coordinate offset
latOffset = 0.0135
lonOffset = 0.0176

# Multiple calls due to api limitations: Est, West, North, South
responseEst = apiCall(centerLatitude, centerLongitude + lonOffset)
responseWest = apiCall(centerLatitude, centerLongitude - lonOffset)
responseNorth = apiCall(centerLatitude + latOffset, centerLongitude)
responseSouth = apiCall(centerLatitude - latOffset, centerLongitude)


if (
    (responseEst.status_code == 200)
    & (responseWest.status_code == 200)
    & (responseNorth.status_code == 200)
    & (responseSouth.status_code == 200)
):
    print("Data obtained correctly.")

    poiMap = {}
    responseInMap(poiMap, responseEst)
    responseInMap(poiMap, responseWest)
    responseInMap(poiMap, responseNorth)
    responseInMap(poiMap, responseSouth)

    printMapLength(poiMap)
    # printMap(poiMap)

else:
    print("Error in obtaining data.")
