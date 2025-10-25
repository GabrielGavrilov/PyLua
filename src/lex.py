from tok_type import TokType
from tok import Tok

class Lexer:
    def __init__(self, src):
        self.src = src + "\n"
        self.src_size = len(self.src)
        self.curr_pos = 0
        self.curr_char = self.src[self.curr_pos]

    def advance(self):
        self.curr_pos += 1

        if self.curr_pos >= self.src_size:
            self.curr_char = '\0'
        else:
            self.curr_char = self.src[self.curr_pos]

    def peek(self):
        if self.curr_pos + 1 >= self.src_size:
            return '\0'
        return self.src[self.curr_pos + 1]
    
    def skip_whitespace(self):
        while self.curr_char == ' ' or self.curr_char == '\t':
            self.advance()

    def generate_tokens(self):
        tokens = []

        while self.curr_char != '\0':
            token = None
            self.skip_whitespace()

            if self.curr_char == '(':
                token = Tok(TokType.LEFT_PAREN, '(')
            
            elif self.curr_char == ')':
                token = Tok(TokType.RIGHT_PAREN, ')')

            elif self.curr_char == '=':
                token = Tok(TokType.EQUALS, '=')

            elif self.curr_char == '+':
                token = Tok(TokType.PLUS, '+')

            elif self.curr_char == '-':
                token = Tok(TokType.MINUS, '-')

            elif self.curr_char == '*':
                token = Tok(TokType.MULTIPLY, '*')

            elif self.curr_char == '/':
                token = Tok(TokType.DIVIDE, '/')

            elif self.curr_char == '\"':
                pass

            elif self.curr_char.isdigit():
                pass

            elif self.curr_char.isalpha():
                pass

            elif self.curr_char == '\n':
                token = Tok(TokType.NEWLINE, '\n')

            self.advance()
            tokens.append(token)

        return tokens