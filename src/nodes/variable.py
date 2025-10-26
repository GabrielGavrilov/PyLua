class VariableNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"(VARIABLE \"{self.name}\" {self.value})"