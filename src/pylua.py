import sys
from scanner import Scanner
from token import TokenType
from parser import Parser
from interpreter import Interpreter
from resolver import Resolver
from callable import Callable

class Test(Callable):
    def arity(self):
        return 2
    
    def call(self, interpreter, arguments):
        return arguments[0] + arguments[1]

if __name__ == "__main__":

    with open(sys.argv[1]) as f:
        src = f.read()

    scanner = Scanner(src)
    parser = Parser(scanner.scan())

    ast = parser.parse()
    # print(ast)

    interpeter = Interpreter()
    resolver = Resolver(interpeter)

    resolver.resolve(ast)

    interpeter.globals.define("add", Test())

    interpeter.interpret(ast)