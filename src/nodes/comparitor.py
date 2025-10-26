from enum import Enum

class Comparitors(Enum):
    LESS_THAN = 1
    GREATER_THAN = 2

class ComparitorNode:
    def __init__(self, left, comparison, right):
        self.left = left
        self.comparison = comparison
        self.right = right

    def __repr__(self):
        return f"(COMPARISON {self.left} {self.comparison} {self.right})"