from enum import Enum, auto

class TokenType(Enum):
    EOF = auto(),
    NEWLINE = auto(),

    LEFT_PAREN = auto(),
    RIGHT_PAREN = auto(),
    EQUALS = auto(),
    GT = auto(),
    LT = auto(),

    PLUS = auto(),
    MINUS = auto(),
    MULTIPLY = auto(),
    DIVIDE = auto(),

    IDENTIFIER = auto(),
    STRING = auto(),
    NUMBER = auto(),

    PRINT = auto()

class Token: 
    def __init__(self, type, value):
        self.type = type
        self.value = value