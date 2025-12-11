from .stmt import *
from .expr import *

class Interpreter:
    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)

    def interpret(self, stmts):
        for stmt in stmts:
            self.execute(stmt)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expr)

        return None

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expr)
        print(value)

        return None