from .token import Token

class Literal:
    def __init__(self, value: any):
        self.value = value

    def __repr__(self):
        return f"(LITERAL {self.value})"

class Binary:
    def __init__(self, left: Literal, operator: Token, right: Literal):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"(BINARY {self.left} {self.operator.type} {self.right})"
    
class VariableExpression:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"(VARIABLE EXPR {self.name.value})"