class ConditionalNode:
    def __init__(self, condition, statement, elseif_blocks=None, else_statement=None):
        self.condition = condition
        self.statement = statement
        self.elseif_blocks = elseif_blocks or []
        self.else_statement = else_statement

    def __repr__(self):
        return f"(CONDITIONAL {self.condition} {self.statement} ELSEIF BLOCKS {self.elseif_blocks} ELSE {self.else_statement})"