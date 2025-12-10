from .token import TokenType, Token

class Scanner:
    def __init__(self, src):
        self.src = src
        self.src_size = len(self.src)
        self.curr_pos = -1
        self.curr_char = None
        self.advance()

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

    def scan_string(self):
        string = ""
        self.advance()
        while self.curr_char != "\"":
            string += self.curr_char
            self.advance()
        
        return Token(TokenType.STRING, string)

    def scan_number(self):
        start_pos = self.curr_pos
        while self.peek().isdigit():
            self.advance()

        number = self.src[start_pos : self.curr_pos + 1]
        return Token(TokenType.NUMBER, number)
    
    def scan_alpha(self):
        start_pos = self.curr_pos
        while self.peek().isalnum():
            self.advance()

        value = self.src[start_pos : self.curr_pos + 1]
        keyword = self.check_keyword(value)
        return Token(keyword, value)
    
    def check_keyword(self, value):
        for token in TokenType:
            if token.name.lower() == value:
                return token
        return TokenType.IDENTIFIER

    def scan(self):
        tokens = []
        while self.curr_char != '\0':
            token = None
            self.skip_whitespace()

            if self.curr_char == '\n':
                token = Token(TokenType.NEWLINE, '\n')

            elif self.curr_char == '(':
                token = Token(TokenType.LEFT_PAREN, '(')
            
            elif self.curr_char == ')':
                token = Token(TokenType.RIGHT_PAREN, ')')

            elif self.curr_char == '=':
                token = Token(TokenType.EQUAL, '=')

            elif self.curr_char == '+':
                token = Token(TokenType.PLUS, '+')

            elif self.curr_char == '-':
                token = Token(TokenType.MINUS, '-')

            elif self.curr_char == '*':
                token = Token(TokenType.MULTIPLY, '*')

            elif self.curr_char == '/':
                token = Token(TokenType.DIVIDE, '/')

            elif self.curr_char == '>':
                token = Token(TokenType.GT, '>')

            elif self.curr_char == '<':
                token = Token(TokenType.LT, '<')

            elif self.curr_char == '\"':
                token = self.scan_string()

            elif self.curr_char.isdigit():
                token = self.scan_number()

            elif self.curr_char.isalpha():
                token = self.scan_alpha()

            self.advance()
            tokens.append(token)
        
        tokens.append(Token(TokenType.EOF, None))
        return tokens