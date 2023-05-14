class Landmark:
    __slots__ = [
        "placeId",
        "name",
        "address",
        "properties",
        "lat",
        "lon",
        "rating",
        "ratingCount",
        "centreDistance",
        "handicapAccessibility",
        "tourismRate",
        "age",
        "surface",
        "height",
        "price",
    ]

    def __init__(
        self,
        placeId: str,
        name: str,
        address: str,
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
        self.properties = properties
        self.lat = lat
        self.lon = lon
        self.rating = rating
        self.ratingCount = ratingCount
        self.centreDistance = centreDistance
        self.handicapAccessibility = handicapAccessibility
        self.tourismRate = tourismRate
        self.age = age
        self.surface = surface
        self.height = height
        self.price = price

    def __str__(self):
        return (
            f"Place id: {self.placeId}\n"
            f"Name: {self.name}\n"
            f"Address: {self.address}\n"
            f"Properties: {self.properties}\n"
            f"Latitude: {self.lat}\n"
            f"Longitude: {self.lon}\n"
            f"Rating: {self.rating}\n"
            f"Rating count: {self.ratingCount}\n"
            f"Centre distance: {self.centreDistance}\n"
            f"Handicap accessibility: {self.handicapAccessibility}\n"
            f"Tourism rate: {self.tourismRate}\n"
            f"Age: {self.age}\n"
            f"Surface: {self.surface}\n"
            f"Height: {self.height}\n"
            f"Price: {self.price}\n"
        )
