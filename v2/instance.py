import sys

class Instance:
    def __init__(self, clazz):
        self.clazz = clazz
        self.fields = {}

    def get(self, name):
        if name in self.fields:
            return self.fields[name.value]
        
        method = self.clazz.find_method(name.value)

        if method is not None:
            return method.bind(self)
        
        sys.exit(f"Undefined property '{name.value}'.")

    def set(self, name, value):
        self.fields[name] = value