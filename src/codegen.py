class CodeGenerator:
    def __init__(self, instructions):
        self.instructions = instructions
        self.code = []
    
    def generate(self):
        for op, arg1, arg2, result in self.instructions:
            if op == '=':
                if isinstance(arg1, str) and not arg1.startswith('"'):
                    # It's a variable, not a constant
                    self.code.append(f"LOAD {arg1}")
                    self.code.append(f"STORE {result}")
                else:
                    self.code.append(f"PUSH {arg1}")
                    self.code.append(f"STORE {result}")
            elif op == '+':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("ADD")
                self.code.append(f"STORE {result}")
            elif op == '-':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("SUB")
                self.code.append(f"STORE {result}")
            elif op == '*':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("MUL")
                self.code.append(f"STORE {result}")
            elif op == '/':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("DIV")
                self.code.append(f"STORE {result}")
            elif op == '<':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("LT")
                self.code.append(f"STORE {result}")
            elif op == '>':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("GT")
                self.code.append(f"STORE {result}")
            elif op == '==':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("EQ")
                self.code.append(f"STORE {result}")
            elif op == '&&':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("AND")
                self.code.append(f"STORE {result}")
            elif op == '||':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"LOAD {arg2}")
                self.code.append("OR")
                self.code.append(f"STORE {result}")
            elif op == 'print':
                self.code.append(f"LOAD {arg1}")
                self.code.append("PRINT")
            elif op == 'label':
                self.code.append(f"LABEL {result}")
            elif op == 'goto':
                self.code.append(f"GOTO {result}")
            elif op == 'if_false':
                self.code.append(f"LOAD {arg1}")
                self.code.append(f"JZ {result}")
        
        return self.code
