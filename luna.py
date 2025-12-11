import sys
from v2.scanner import Scanner
from v2.token import TokenType
from v2.parser import Parser
from v2.interpreter import Interpreter

if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        src = f.read()

    # src = "local a = 8\nprint(a)"

    scanner = Scanner(src)
    parser = Parser(scanner.scan())

    ast = parser.parse()
    # print(ast)
    interpeter = Interpreter()

    interpeter.interpret(ast)