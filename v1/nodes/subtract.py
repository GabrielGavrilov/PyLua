class SubtractNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(SUBTRACT {self.left} {self.right})"
