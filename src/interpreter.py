from nodes.number import NumberNode
from nodes.add import AddNode
from nodes.subtract import SubtractNode
from nodes.print import PrintNode
from nodes.string import StringNode

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        for node in ast:
            self.eval(node)

    def eval(self, node):
        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, AddNode):
            return self.eval(node.left) + self.eval(node.right)

        if isinstance(node, SubtractNode):
            return self.eval(node.left) - self.eval(node.right)
        
        if isinstance(node, PrintNode):
            print(self.eval(node.value))