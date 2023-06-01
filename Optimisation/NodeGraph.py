class NodeGraph:
    __slots__ = ["name", "coveredDistance", "remainingBudget", "remainingTime"]

    def __init__(
        self, name: str, coveredDistance: int, remainingBudget: int, remainingTime: int
    ):
        self.name = name
        self.coveredDistance = coveredDistance
        self.remainingBudget = remainingBudget
        self.remainingTime = remainingTime

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Covered Distance: {self.coveredDistance}\n"
            f"Remaining Budget: {self.remainingBudget}\n"
            f"Remaining Time: {self.remainingTime}\n"
        )
