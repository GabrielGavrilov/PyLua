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

    def gen_string_token(self):
        string = ""
        self.advance()
        while self.curr_char != "\"":
            string += self.curr_char
            self.advance()
        
        return Tok(TokType.STRING, string)

    def gen_number_token(self):
        start_pos = self.curr_pos
        while self.peek().isdigit():
            self.advance()

        number = self.src[start_pos : self.curr_pos + 1]
        return Tok(TokType.NUMBER, number)

    def gen_alpha_token(self):
        start_pos = self.curr_pos
        while self.peek().isalnum():
            self.advance()

        value = self.src[start_pos : self.curr_pos + 1]
        keyword = self.check_keyword(value)
        return Tok(keyword, value)

    def check_keyword(self, value):
        for token in TokType:
            if token.name.lower() == value:
                return token
        return TokType.IDENTIFIER

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

            elif self.curr_char == '>':
                token = Tok(TokType.GT, '>')

            elif self.curr_char == '<':
                token = Tok(TokType.LT, '<')

            elif self.curr_char == '\"':
                token = self.gen_string_token()

            elif self.curr_char.isdigit():
                token = self.gen_number_token()

            elif self.curr_char.isalpha():
                token = self.gen_alpha_token()

            elif self.curr_char == '\n':
                token = Tok(TokType.NEWLINE, '\n')

            self.advance()
            tokens.append(token)
            
        return tokens