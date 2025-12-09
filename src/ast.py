class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class LetStatement(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class RepeatStatement(ASTNode):
    def __init__(self, count, block):
        self.count = count
        self.block = block

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
