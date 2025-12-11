from abc import ABC, abstractmethod
from .token import Token

class ExprVisitor(ABC):
    @abstractmethod
    def visit_literal_expr(self, expr):
        pass

    @abstractmethod
    def visit_binary_expr(self, left, operator, right):
        pass

    @abstractmethod
    def visit_variable_expr(self, name):
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

class Binary(Expr):
    def __init__(self, left: Literal, operator: Token, right: Literal):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

    def __repr__(self):
        return f"(BINARY {self.left} {self.operator.type} {self.right})"
    
class VariableExpression(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

    def __repr__(self):
        return f"(VARIABLE EXPR {self.name.value})"