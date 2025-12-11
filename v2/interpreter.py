from .stmt import *
from .expr import *
from .token import TokenType

class Interpreter:
    def __init__(self):
        self.locals = {}

    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)

    def interpret(self, stmts):
        for stmt in stmts:
            self.execute(stmt)

    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type is TokenType.PLUS:
            return left + right
    
    def visit_variable_expr(self, expr):
        return self.look_up_variable(expr.name, expr)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expr)

        return None

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expr)
        print(value)

        return None
    
    def visit_variable_stmt(self, stmt):
        value = None
        if (stmt.initializer is not None):
            value = self.evaluate(stmt.initializer)

        self.locals[stmt.name.value] = value

        return None
    
    def look_up_variable(self, name, expr):
        return self.locals[name.value]