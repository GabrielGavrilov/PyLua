import sys
from tok_type import TokType
from tok import Tok
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        src = f.read()

    # src = "print(\"Hello, World!\")"

    lex = Lexer(src)
    tokens = lex.generate_tokens()

    parser = Parser(tokens)
    ast = parser.program()

    # for i in ast:
    #     print(i)

    Interpreter(ast)
