from abc import ABC, abstractmethod

class StmtVisitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, expr):
        pass
    
    @abstractmethod
    def visit_print_stmt(self, expr):
        pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Expression(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

    def __repr__(self):
        return f"(EXPRESSION {self.value})"
    
class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

    def __repr__(self):
        return f"(PRINT {self.expr})"
    
class VariableStatement:
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        return f"(VARIABLE STATEMENT {self.name.value} {self.initializer})"