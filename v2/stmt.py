class Expression:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"(EXPRESSION {self.value})"
    
class Print:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"(PRINT {self.expr})"