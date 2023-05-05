class Landmark:
    def __init__(
        self,
        name: str,
        centreDistance: float,
        refWiki: str,
        properties: list,
        lat: float,
        lon: float,
    ):
        self.name = name
        self.centreDistance = centreDistance
        self.refWiki = refWiki
        self.properties = properties
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"Landmark(name = {self.name}, centreDistance = {self.centreDistance}, refWiki = {self.refWiki}, properties = {self.properties}, lat = {self.lat}, lon = {self.lon})"
