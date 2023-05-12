class Landmark:
    __slots__ = [
        "name",
        "properties",
        "lat",
        "lon",
        "rating",
        "ratingCount",
        "centreDistance",  # da popolare
        "handicapAccessibility",  # da popolare
        "tourismRate",
        "age",
        "surface",
        "height",
        "price",
    ]

    def __init__(
        self,
        name: str,
        properties: list,
        lat: float,
        lon: float,
        rating: float,
        ratingCount: int,
    ):
        self.name = name
        self.properties = properties
        self.lat = lat
        self.lon = lon
        self.rating = rating
        self.ratingCount = ratingCount

    def setTourismRate(self, tourismRate):
        self.tourismRate = tourismRate

    def setAge(self, age):
        self.age = age

    def setSurface(self, surface):
        self.surface = surface

    def setHeight(self, height):
        self.height = height

    def setPrice(self, price):
        self.price = price

    def __str__(self):
        return f"Landmark(name = {self.name}, properties = {self.properties}, lat = {self.lat}, lon = {self.lon}, rating = {self.rating}, ratingCount = {self.ratingCount})"
