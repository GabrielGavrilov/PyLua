class FunctionNode:
    def __init__(self, name, statement):
        self.name = name
        self.statement = statement

    def __repr__(self):
        return f"(FUNCTION {self.name} {self.statement})"