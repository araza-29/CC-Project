from ast import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
    
    def analyze(self, node):
        method_name = f'analyze_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_analyze)
        return method(node)
    
    def generic_analyze(self, node):
        raise Exception(f"No analyze method for {type(node).__name__}")
    
    def analyze_Program(self, node):
        for stmt in node.statements:
            self.analyze(stmt)
    
    def analyze_LetStatement(self, node):
        expr_type = self.analyze(node.expression)
        
        if node.identifier in self.symbol_table:
            # Variable reassignment - check type compatibility
            if self.symbol_table[node.identifier] != expr_type:
                raise Exception(f"Type mismatch: variable '{node.identifier}' is {self.symbol_table[node.identifier]}, cannot assign {expr_type}")
        else:
            # New variable declaration
            self.symbol_table[node.identifier] = expr_type
    
    def analyze_IfStatement(self, node):
        cond_type = self.analyze(node.condition)
        if cond_type != 'bool':
            raise Exception(f"If condition must be boolean, got {cond_type}")
        
        for stmt in node.then_block:
            self.analyze(stmt)
        
        if node.else_block:
            for stmt in node.else_block:
                self.analyze(stmt)
    
    def analyze_RepeatStatement(self, node):
        count_type = self.analyze(node.count)
        if count_type != 'int':
            raise Exception(f"Repeat count must be integer, got {count_type}")
        
        for stmt in node.block:
            self.analyze(stmt)
    
    def analyze_PrintStatement(self, node):
        self.analyze(node.expression)
    
    def analyze_BinaryOp(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        
        if node.operator in ['+', '-', '*', '/']:
            if left_type != 'int' or right_type != 'int':
                raise Exception(f"Arithmetic requires int operands, got {left_type} and {right_type}")
            return 'int'
        elif node.operator in ['<', '>', '==']:
            if left_type != right_type:
                raise Exception(f"Comparison requires same types, got {left_type} and {right_type}")
            return 'bool'
        elif node.operator in ['&&', '||']:
            if left_type != 'bool' or right_type != 'bool':
                raise Exception(f"Logical operators require bool operands, got {left_type} and {right_type}")
            return 'bool'
        else:
            raise Exception(f"Unknown operator: {node.operator}")
    
    def analyze_Number(self, node):
        return 'int'
    
    def analyze_String(self, node):
        return 'string'
    
    def analyze_Boolean(self, node):
        return 'bool'
    
    def analyze_Identifier(self, node):
        if node.name not in self.symbol_table:
            raise Exception(f"Undefined variable: {node.name}")
        return self.symbol_table[node.name]
