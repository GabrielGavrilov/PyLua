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

    def visit_variable_expr(self, expr):
        if self.scopes:
            scope = self.scopes[-1]
            if not len(self.scopes) == 0 and scope[expr.name.value] == False:
                sys.exit("Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)
        return None

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.value in self.scopes[i]:
                self.interpeter.resolve(expr, len(self.scopes) - 1 - i)
                return

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

    def visit_binary_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None
    
    def visit_literal_expr(self, expr):
        return None