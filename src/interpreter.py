from nodes.number import NumberNode
from nodes.add import AddNode
from nodes.subtract import SubtractNode
from nodes.print import PrintNode
from nodes.string import StringNode
from nodes.variable import VariableNode
from nodes.conditional import ConditionalNode
from nodes.comparitor import ComparitorNode, Comparitors
from nodes.boolean import BooleanNode

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

        if isinstance(node, BooleanNode):
            return node.value
        
        if isinstance(node, ComparitorNode):
            if node.comparison == Comparitors.GREATER_THAN:
                return self.eval(node.left) > self.eval(node.right)
            if node.comparison == Comparitors.LESS_THAN:
                return self.eval(node.left) < self.eval(node.right)

        if isinstance(node, AddNode):
            return self.eval(node.left) + self.eval(node.right)

        if isinstance(node, SubtractNode):
            return self.eval(node.left) - self.eval(node.right)
        
        if isinstance(node, VariableNode):
            return self.eval(node.value)

        if isinstance(node, PrintNode):
            print(self.eval(node.value))

        if isinstance(node, ConditionalNode):
            if self.eval(node.condition):
                for statement in node.statement:
                    self.eval(statement)
                    
            elif node.elseif_blocks:
                for elseif_statements in node.elseif_blocks:
                    self.eval(elseif_statements)
            else:
                if node.else_statement:
                    for else_statement in node.else_statement:
                        self.eval(else_statement)