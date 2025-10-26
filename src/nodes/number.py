class NumberNode:
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"(NUMBER {self.value})"