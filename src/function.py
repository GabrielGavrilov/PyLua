from environment import Environment
from Return import Return
from callable import Callable

class Function(Callable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return Function(self.declaration, environment, self.is_initializer)
    
    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            arg_name = self.declaration.params[i].value
            environment.define(arg_name, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body.statements, environment)
        
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
        
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        
        return None