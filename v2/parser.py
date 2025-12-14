import sys
from .token import Token, TokenType
from .scanner import Scanner
from .stmt import *
from .expr import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.statements = []

    def parse(self):
        while not self.is_at_end():
            self.statements.append(self.declaration())
        return self.statements

    def abort(self, message):
        sys.exit(f"[Parsing error]: {message}")

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def advance(self) -> None:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def check(self, type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def match(self, type: TokenType) -> bool:
        if self.check(type):
            self.advance()
            return True
        return False
    
    def consume(self, type):
        if self.check(type):
            return self.advance()
        self.abort(f"Expected {type} but got {self.peek().type}")

    def consume_newline(self):
        while self.check(TokenType.NEWLINE):
            self.advance()
    
    def print_statement(self):
        self.consume(TokenType.LEFT_PAREN)
        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN)
        return Print(expr)
    
    def if_statement(self):
        condition = self.expression()
        self.consume(TokenType.THEN)
        then_branch = self.statement()
        else_branch = None

        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        self.consume(TokenType.END)
        return IfStatement(condition, then_branch, else_branch)

    
    def local_declaration(self):
        name = self.consume(TokenType.IDENTIFIER)

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        return VariableStatement(name, initializer)

    def function_declaration(self):
        name = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.LEFT_PAREN)
        params = []

        self.consume(TokenType.RIGHT_PAREN)
        body = self.block_statements()
        return FunctionStatement(name, params, body)

    def block_statements(self):
        statements = []

        while not self.check(TokenType.END) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.END)
        return statements

    def declaration(self):
        if self.match(TokenType.LOCAL):
            return self.local_declaration()
        
        if self.match(TokenType.FUNCTION):
            return self.function_declaration()

        return self.statement()
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        
        if self.match(TokenType.IF):
            return self.if_statement()

        return self.expression_statement()
    
    def expression_statement(self):
        expr = self.expression()
        return Expression(expr)

    def expression(self):
        return self.assignment()
    
    def assignment(self):
        return self.or_assignment()

    def or_assignment(self):
        return self.and_assignment()

    def and_assignment(self):
        return self.equality()

    def equality(self):
        return self.comparison()

    def comparison(self):
        expr = self.term()

        if self.match(TokenType.GT):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr
    
    def term(self):
        expr = self.call()

        if self.match(TokenType.PLUS):
            operator = self.previous()
            right = self.primary()
            expr = Binary(expr, operator, right)

        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.primary()
            expr = Binary(expr, operator, right)

        return expr
    
    def finish_call(self, callee):
        arguments = []

        paren = self.consume(TokenType.RIGHT_PAREN)

        return CallExpression(callee, paren, arguments)

    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def primary(self):
        if self.match(TokenType.NUMBER) or self.match(TokenType.STRING):
            return Literal(self.previous().value)
        
        if self.match(TokenType.IDENTIFIER):
            return VariableExpression(self.previous())