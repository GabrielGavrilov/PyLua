class StringNode:
    def __init__(self, value):
        self.value = value

    def __repl__(self):
        return f"(STRING {self.value})"