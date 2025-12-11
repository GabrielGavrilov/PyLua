from abc import ABC, abstractmethod
from .token import Token

class ExprVisitor(ABC):
    @abstractmethod
    def visit_literal_expr(self, expr):
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)
    
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