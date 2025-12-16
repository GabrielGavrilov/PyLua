import sys
from .stmt import *
from .expr import *
from .token import TokenType
from .environment import Environment
from .function import Function
from .Return import Return

class Interpreter:
    def __init__(self):
        self.locals = {}
        self.globals = Environment()
        self.environment = self.globals

    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    def resolve(self, expr, depth):
        self.locals[expr] = depth

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
        
        if expr.operator.type is TokenType.LT:
            return left < right

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

    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        args = []

        for arg in expr.arguments:
            args.append(self.evaluate(arg))

        function = callee

        if len(args) != function.arity():
            sys.exit(f"Expected {function.arity()} arguments but got {len(args)}.")

        return function.call(self, args)

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

        self.environment.define(stmt.name.value, value)
        return None

    def visit_if_stmt(self, stmt):
        if (self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

        return None
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        None

    def visit_function_stmt(self, stmt):
        function = Function(stmt, self.environment, False)
        self.environment.define(stmt.name.value, function)
        return None
    
    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)