from enum import Enum, auto

class TokenType(Enum):
    EOF = auto(),
    NEWLINE = auto(),

    LEFT_PAREN = auto(),
    RIGHT_PAREN = auto(),
    EQUAL = auto(),
    EQUAL_EQUAL = auto()
    GT = auto(),
    LT = auto(),
    COMMA = auto()

    PLUS = auto(),
    MINUS = auto(),
    MULTIPLY = auto(),
    DIVIDE = auto(),

    IDENTIFIER = auto(),
    STRING = auto(),
    NUMBER = auto(),

    LOCAL = auto()
    PRINT = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    END = auto()
    FUNCTION = auto()

class Token: 
    def __init__(self, type, value):
        self.type = type
        self.value = value