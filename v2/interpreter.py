from .stmt import *
from .expr import *
from .token import TokenType
from .environment import Environment

class Interpreter:
    def __init__(self):
        self.locals = {}
        self.globals = Environment()
        self.environment = self.globals

    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr, depth):
        self.locals.put(expr, depth)

    def interpret(self, stmts):
        for stmt in stmts:
            self.execute(stmt)

    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type is TokenType.GT:
            return left > right
        if expr.operator.type is TokenType.MINUS:
            return left - right
        if expr.operator.type is TokenType.PLUS:
            return left + right
    
    def visit_variable_expr(self, expr):
        return self.look_up_variable(expr.name, expr)
    
    def look_up_variable(self, name, expr):
        distance = self.locals.get(expr)

        if distance is not None:
            return self.environment.get_at(distance, name.value)
        else:
            return self.globals.get(name)

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

    def visit_if_stmt(self, stmt):
        if (self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

        return None