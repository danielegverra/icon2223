class Landmark:
    __slots__ = [
        "placeId",
        "name",
        "address",
        "type",
        "properties",
        "lat",
        "lon",
        "rating",
        "highlyRated",
        "ratingCount",
        "popular",
        "highlyRecommended",
        "centreDistance",
        "closeToCityCentre",
        "handicapAccessibility",
        "tourismRate",
        "tourismRateOutOfTen",
        "topTourismAttraction",
        "age",
        "ancient",
        "surface",
        "height",
        "impressive",
        "price",
        "cheap",
        "density",
        "timeToVisit",
        "tourismPriority",
    ]

    def __init__(
        self,
        placeId: str,
        name: str,
        address: str,
        type: str,
        properties: list,
        lat: float,
        lon: float,
        rating: float,
        ratingCount: int,
        centreDistance: float,
        handicapAccessibility: bool,
        tourismRate: int,
        age: int,
        surface: float,
        height: float,
        price: int,
    ):
        self.placeId = placeId
        self.name = name
        self.address = address
        self.type = type
        self.properties = properties
        self.lat = lat
        self.lon = lon
        self.rating = rating
        self.highlyRated = None
        self.ratingCount = ratingCount
        self.popular = None
        self.highlyRecommended = None
        self.centreDistance = centreDistance
        self.closeToCityCentre = None
        self.handicapAccessibility = handicapAccessibility
        self.tourismRate = tourismRate
        self.tourismRateOutOfTen = None
        self.topTourismAttraction = None
        self.age = age
        self.ancient = None
        self.surface = surface
        self.height = height
        self.impressive = None
        self.price = price
        self.cheap = None
        self.density = None
        self.timeToVisit = None
        self.tourismPriority = None

    def __str__(self):
        return (
            f"Place id: {self.placeId}\n"
            f"Name: {self.name}\n"
            f"Address: {self.address}\n"
            f"Type: {self.type}\n"
            f"Properties: {self.properties}\n"
            f"Latitude: {self.lat}\n"
            f"Longitude: {self.lon}\n"
            f"Rating: {self.rating}\n"
            f"HighlyRated: {self.highlyRated}\n"
            f"Rating count: {self.ratingCount}\n"
            f"Popular: {self.popular}\n"
            f"HighlyRecommended: {self.highlyRecommended}\n"
            f"Centre distance: {self.centreDistance}\n"
            f"CloseToCityCentre: {self.closeToCityCentre}\n"
            f"Handicap accessibility: {self.handicapAccessibility}\n"
            f"Tourism rate: {self.tourismRate}\n"
            f"TurismRateOutOfTen: {self.tourismRateOutOfTen}\n"
            f"TopTourismAttraction: {self.topTourismAttraction}\n"
            f"Age: {self.age}\n"
            f"Ancient: {self.ancient}\n"
            f"Surface: {self.surface}\n"
            f"Height: {self.height}\n"
            f"Impressive: {self.impressive}\n"
            f"Price: {self.price}\n"
            f"Cheap: {self.cheap}\n"
            f"Density: {self.density}\n"
            f"timeToVisit: {self.timeToVisit}\n"
            f"tourismPriority: {self.tourismPriority}\n"
        )
