from ast import *

class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
    
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"
    
    def emit(self, op, arg1=None, arg2=None, result=None):
        self.instructions.append((op, arg1, arg2, result))
    
    def generate(self, node):
        method_name = f'generate_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_generate)
        return method(node)
    
    def generic_generate(self, node):
        raise Exception(f"No generate method for {type(node).__name__}")
    
    def generate_Program(self, node):
        for stmt in node.statements:
            self.generate(stmt)
        return self.instructions
    
    def generate_LetStatement(self, node):
        expr_temp = self.generate(node.expression)
        self.emit('=', expr_temp, None, node.identifier)
    
    def generate_IfStatement(self, node):
        cond_temp = self.generate(node.condition)
        else_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('if_false', cond_temp, None, else_label)
        
        for stmt in node.then_block:
            self.generate(stmt)
        
        self.emit('goto', None, None, end_label)
        self.emit('label', None, None, else_label)
        
        if node.else_block:
            for stmt in node.else_block:
                self.generate(stmt)
        
        self.emit('label', None, None, end_label)
    
    def generate_RepeatStatement(self, node):
        count_temp = self.generate(node.count)
        counter = self.new_temp()
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('=', 0, None, counter)
        self.emit('label', None, None, start_label)
        
        cond_temp = self.new_temp()
        self.emit('<', counter, count_temp, cond_temp)
        self.emit('if_false', cond_temp, None, end_label)
        
        for stmt in node.block:
            self.generate(stmt)
        
        self.emit('+', counter, 1, counter)
        self.emit('goto', None, None, start_label)
        self.emit('label', None, None, end_label)
    
    def generate_PrintStatement(self, node):
        expr_temp = self.generate(node.expression)
        self.emit('print', expr_temp, None, None)
    
    def generate_BinaryOp(self, node):
        left_temp = self.generate(node.left)
        right_temp = self.generate(node.right)
        result_temp = self.new_temp()
        self.emit(node.operator, left_temp, right_temp, result_temp)
        return result_temp
    
    def generate_Number(self, node):
        temp = self.new_temp()
        self.emit('=', node.value, None, temp)
        return temp
    
    def generate_String(self, node):
        temp = self.new_temp()
        self.emit('=', f'"{node.value}"', None, temp)
        return temp
    
    def generate_Boolean(self, node):
        temp = self.new_temp()
        self.emit('=', node.value, None, temp)
        return temp
    
    def generate_Identifier(self, node):
        return node.name
