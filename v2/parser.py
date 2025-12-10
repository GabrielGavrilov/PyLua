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
    
    def local_declaration(self):
        name = self.consume(TokenType.IDENTIFIER)

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        return VariableStatement(name, initializer)

    def declaration(self):
        if self.match(TokenType.LOCAL):
            return self.local_declaration()

        self.consume_newline()
        return self.statement()
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()
    
    def expression_statement(self):
        expr = self.expression()
        return Expression(expr)

    def expression(self):
        return self.term()
    
    def term(self):
        expr = self.primary()

        if self.match(TokenType.PLUS):
            operator = self.previous()
            right = self.primary()
            expr = Binary(expr, operator, right)

        return expr

    def primary(self):
        if self.match(TokenType.NUMBER) or self.match(TokenType.STRING):
            return Literal(self.previous().value)
        
        if self.match(TokenType.IDENTIFIER):
            return VariableExpression(self.previous())