import sys

class Environment:
    def __init__(self, enclosing = None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance):
        environment = self

        for i in range(distance):
            environment = environment.enclosing
        
        return environment
    
    def get_at(self, distance, name):
        return self.ancestor(distance).values[name]
    
    def assign_at(self, distance, name, value):
        self.ancestor(distance).values[name.value] = value

    def get(self, name):
        if name.value in self.values:
            return self.values[name.value]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
                
        sys.exit(f"[Runtime error]: Undefined variable {name.value}")

    def assign(self, name, value):
        if name.value in self.values:
            self.values[name.value] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        sys.exit(f"[Runtime error]: Undefined variable {name.value}")