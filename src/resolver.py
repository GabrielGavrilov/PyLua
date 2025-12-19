import sys
from enum import Enum, auto

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()

class Resolver: 
    def __init__(self, interpreter):
        self.interpeter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, stmt):
        stmt.accept(self)

    def resolve_expr(self, expr):
        expr.accept(self)

    def declare(self, name):
        if len(self.scopes) == 0:
            return
        
        scope = self.scopes[-1]
    
        if name.value in scope:
            sys.exit("Variable already exists with the same name in this scope.")

        scope[name.value] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.value] = True

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def visit_variable_stmt(self, stmt):
        self.declare(stmt.name)

        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)

        self.define(stmt.name)
        return None
    
    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def resolve_function(self, function, type):
        enclosing_function = self.current_function
        self.current_function = type

        self.begin_scope()
        
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body.statements)
        self.end_scope()
        self.current_function = enclosing_function

    def visit_variable_expr(self, expr):
        if self.scopes:
            scope = self.scopes[-1]
            if expr.name.value in scope and scope[expr.name.value] is False:
                sys.exit("Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)
        return None

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.value in self.scopes[i]:
                self.interpeter.resolve(expr, len(self.scopes) - 1 - i)
                return
            
    def visit_expression_stmt(self, stmt):
        self.resolve_expr(stmt.expr)
        return None

    def visit_print_stmt(self, stmt):
        self.resolve_expr(stmt.expr)
        return None
    
    def visit_if_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_stmt(stmt.else_branch)
        return None
    
    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None

    def visit_return_stmt(self, stmt):
        if self.current_function is FunctionType.NONE:
            sys.exit("Can't return from outside a function")

        if stmt.value is not None:
            if self.current_function is FunctionType.INITIALIZER:
                sys.exit("Can't return a value from an initializer")
            
            self.resolve_expr(stmt.value)
        
        return None

    def visit_while_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)
        return None

    def visit_binary_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None
    
    def visit_literal_expr(self, expr):
        return None
    
    def visit_call_expr(self, expr):
        self.resolve_expr(expr.callee)

        for arg in expr.arguments:
            self.resolve_expr(arg)

        return None
    
    def visit_assign_expr(self, expr):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)
        return None