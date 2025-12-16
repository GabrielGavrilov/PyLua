from .instance import Instance

class LuaClass:
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        
        if self.superclass is not None:
            return self.superclass.find_method(name)
        
        return None

    def artity(self):
        initializer = self.find_method("init")
        
        if initializer is None:
            return 0
        
        return initializer.arity()
    
    def call(self, interpreter, arguments):
        instance = Instance(self)
        initializer = self.find_method("init")

        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance