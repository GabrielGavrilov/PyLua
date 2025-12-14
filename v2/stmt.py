from abc import ABC, abstractmethod

class StmtVisitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, expr):
        pass
    
    @abstractmethod
    def visit_print_stmt(self, expr):
        pass

    @abstractmethod
    def visit_variable_stmt(self, name, initializer):
        pass

    @abstractmethod
    def visit_if_stmt(self, expr):
        pass

    @abstractmethod
    def visit_function_stmt(self, expr):
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
        return f"(EXPRESSION {self.expr})"
    
class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

    def __repr__(self):
        return f"(PRINT {self.expr})"
    
class VariableStatement(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_variable_stmt(self)

    def __repr__(self):
        return f"(VARIABLE STATEMENT {self.name.value} {self.initializer})"
    
class IfStatement(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)
    
    def __repr__(self):
        return f"(IF STATEMENT {self.condition} THEN {self.then_branch} ELSE {self.else_branch})"

class FunctionStatement(Stmt):
    def __init__(self, name, params = [], body = []):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)

    def __repr__(self):
        return f"(FUNCTION STATEMENT {self.name.value} PARAMS {self.params} BODY {self.body})"