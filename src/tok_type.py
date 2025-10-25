from enum import Enum

class TokType(Enum):
    EOF = -1
    NEWLINE = 0

    # Keywords
    PRINT = 100

    # Operators
    LEFT_PAREN = 200
    RIGHT_PAREN = 201
    EQUALS = 202

    # Arithmetic
    PLUS = 300
    MINUS = 301
    MULTIPLY = 302
    DIVIDE = 303

    # Data types
    IDENTIFIER = 400
    STRING = 401
    NUMBER = 402