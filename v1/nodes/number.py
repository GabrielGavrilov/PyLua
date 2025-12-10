class NumberNode:
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"(NUMBER {self.value})"
    
class AddNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"(ADD {self.left} {self.right})"
