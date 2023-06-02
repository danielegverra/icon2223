class NodeGraph:
    __slots__ = [
        "name",
        "coveredDistance",
        "remainingBudget",
        "remainingTime",
        "visitedNodes",
    ]

    def __init__(
        self,
        name: str,
        coveredDistance: int,
        remainingBudget: int,
        remainingTime: int,
        visitedNodes: list[str],
    ):
        self.name = name
        self.coveredDistance = coveredDistance
        self.remainingBudget = remainingBudget
        self.remainingTime = remainingTime
        self.visitedNodes = visitedNodes

    def __str__(self):
        return (
            f"{self.name}"
            # f"Name: {self.name}\n"
            # f"Covered Distance: {self.coveredDistance}\n"
            # f"Remaining Budget: {self.remainingBudget}\n"
            # f"Remaining Time: {self.remainingTime}\n"
            # f"Visited Nodes: {self.visitedNodes}"
        )
