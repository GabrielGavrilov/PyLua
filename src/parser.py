import sys
from tok import Tok;
from tok_type import TokType;

from nodes.number import NumberNode
from nodes.add import AddNode
from nodes.subtract import SubtractNode
from nodes.print import PrintNode
from nodes.string import StringNode
from nodes.variable import VariableNode
from nodes.boolean import BooleanNode
from nodes.conditional import ConditionalNode
from nodes.comparitor import Comparitors, ComparitorNode
from nodes.function import FunctionNode

class Parser:
    def __init__(self, tokens):
        self.variables = set()
        self.functions = set()

        self.tokens = tokens
        self.tokens_size = len(tokens)
        self.curr_pos = -1
        self.current_tok = None
        self.peek_tok = None

        self.advance()
        self.advance()
        
    def abort(self, message):
        sys.exit(f"[Luna parsing error]: {message}")

    def check(self, type):
        return type == self.current_tok.type

    def check_peek(self, type):
        return type == self.peek_tok.type

    def match(self, type):
        if not self.check(type):
            self.abort(f"Expected {type}, got {self.current_tok.type}")

    def advance(self):
        self.curr_pos += 1

        if self.curr_pos >= self.tokens_size:
            self.current_tok = self.peek_tok
            self.peek_tok = Tok(TokType.EOF, None)
        else:
            self.current_tok = self.peek_tok
            self.peek_tok = self.tokens[self.curr_pos]

    def newline(self):
        while self.check(TokType.NEWLINE):
            self.advance()

    def program(self):
        ast = []
        while self.check(TokType.NEWLINE):
            self.advance()

        while not self.check(TokType.EOF):
            ast.append(self.statement())
        
        return ast

    def statement(self):
        result = self.expression()

        if self.current_tok.type == TokType.PRINT:
            self.advance()
            result = PrintNode(self.expression())

        if self.current_tok.type == TokType.IDENTIFIER:
            if self.check_peek(TokType.EQUALS):
                name = self.current_tok.value
                self.advance()
                result = VariableNode(name, self.statement())
                self.variables.add(result)

        if self.current_tok.type == TokType.FUNCTION:
            self.advance()
            # functio name
            statements = []
            name = self.current_tok.value
        
            self.advance()
            # skip () for now
            self.advance()
            self.advance()
            # skip newline
            self.advance()

            while not self.check(TokType.END):
                statements.append(self.statement())

            self.advance()
            self.functions.add(FunctionNode(name, statements))

        if self.current_tok.type == TokType.EQUALS:
            self.advance()
            result = self.expression()

        if self.current_tok.type == TokType.IF:
            self.advance()
            condition = self.statement()
            statements = []
            elseif_statements = []
            else_statements = []

            while not self.check(TokType.END) and not self.check(TokType.ELSEIF) and not self.check(TokType.ELSE):
                statements.append(self.statement())

            if self.check(TokType.ELSEIF):
                while not self.check(TokType.END) and not self.check(TokType.ELSE):
                    self.advance()
                    elseif_condition = self.statement()
                    statements = []

                    while not self.check(TokType.END) and not self.check(TokType.ELSEIF) and not self.check(TokType.ELSE):
                        statements.append(self.statement())
                    
                    elseif_statements.append(ConditionalNode(elseif_condition, statements))

            if self.check(TokType.ELSE):
                self.advance()
                self.advance()
                while not self.check(TokType.END):
                    else_statements.append(self.statement())

            self.advance()
            result = ConditionalNode(condition, statements, elseif_statements if len(elseif_statements) > 0 else None, else_statements if len(else_statements) > 0 else None)

        if self.current_tok.type == TokType.ELSE:
            self.advance()

        if self.current_tok.type == TokType.THEN:
            self.advance()
        
        self.newline()
        return result

    def expression(self):
        result = self.term()

        if self.current_tok.type == TokType.GT:
            self.advance()
            result = ComparitorNode(result, Comparitors.GREATER_THAN, self.factor())

        if self.current_tok.type == TokType.PLUS:
            self.advance()
            result = AddNode(result, self.factor())

        if self.current_tok.type == TokType.MINUS:
            self.advance()
            result = SubtractNode(result, self.factor())
            
        return result

    def term(self):
        result = self.factor()

        return result

    def factor(self):
        token = self.current_tok

        if token.type == TokType.LEFT_PAREN:
            self.advance()
            result = self.statement()
            self.match(TokType.RIGHT_PAREN)
            self.advance()
            return result

        if token.type == TokType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        if token.type == TokType.STRING:
            self.advance()
            return StringNode(token.value)
        
        if token.type == TokType.TRUE or token.type == TokType.FALSE:
            self.advance()
            return BooleanNode(token.value)

        if token.type == TokType.IDENTIFIER:
            for var in self.variables:
                if var.name == token.value:
                    self.advance()
                    return VariableNode(var.name, var.value)
            for func in self.functions:
                if func.name == token.value:
                    self.advance()
                    return FunctionNode(func.name, func.statement)
                