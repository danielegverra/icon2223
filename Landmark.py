class Landmark:
    def __init__(
        self,
        name: str,
        # centreDistance: float,
        # refWiki: str,
        properties: list,
        lat: float,
        lon: float,
        rating: float,
        ratingCount: int,
    ):
        self.name = name
        # self.centreDistance = centreDistance
        # self.refWiki = refWiki
        self.properties = properties
        self.lat = lat
        self.lon = lon
        self.rating = rating
        self.ratingCount = ratingCount

    def __str__(self):
        return f"Landmark(name = {self.name}, properties = {self.properties}, lat = {self.lat}, lon = {self.lon}, rating = {self.rating}, ratingCount = {self.ratingCount})"
