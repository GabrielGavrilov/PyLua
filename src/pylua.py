import sys
from scanner import Scanner
from token import TokenType
from parser import Parser
from interpreter import Interpreter
from resolver import Resolver

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        src = f.read()

    scanner = Scanner(src)
    parser = Parser(scanner.scan())

    ast = parser.parse()
    #print(ast)

    interpeter = Interpreter()
    resolver = Resolver(interpeter)

    resolver.resolve(ast)
    interpeter.interpret(ast)