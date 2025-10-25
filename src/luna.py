from tok_type import TokType
from tok import Tok
from lex import Lexer

if __name__ == "__main__":

    src = "()=+-*/"

    lex = Lexer(src)
    tokens = lex.generate_tokens()

    for i in tokens:
        print(i.type)