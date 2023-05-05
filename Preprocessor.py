import requests as rq

from Landmark import Landmark

response = rq.get(
    "https://api.opentripmap.com/0.1/en/places/radius?radius=7000&lon=12.4762505&lat=41.8995134&rate=3&format=json&limit=2000&apikey=5ae2e3f221c38a28845f05b6c4fa232e8d7430baddba0e7f4d0e6941"
)

if response.status_code == 200:
    print("data obtained correctly")
    data = response.json()
    poiMap = {}

    for element in data:
        poi = Landmark(
            element["xid"],
            element["name"],
            None,
            element["wikidata"],
            element["kinds"],
            element["point"]["lat"],
            element["point"]["lon"],
        )
        # print(poi)
        poiMap[poi.id] = poi

    """
    for key, value in poiMap.items():
        print()
        print(key)
        print(value)
        print()
    """
    # print(poiMap.__len__())


else:
    print("error data reception")
