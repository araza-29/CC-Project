class VirtualMachine:
    def __init__(self, code):
        self.code = code
        self.stack = []
        self.memory = {}
        self.pc = 0
        self.labels = {}
        
        # Build label map
        for i, instruction in enumerate(code):
            if instruction.startswith('LABEL'):
                label = instruction.split()[1]
                self.labels[label] = i
    
    def run(self):
        while self.pc < len(self.code):
            instruction = self.code[self.pc]
            parts = instruction.split(maxsplit=1)
            op = parts[0]
            
            if op == 'PUSH':
                value = parts[1]
                if value == 'True':
                    self.stack.append(True)
                elif value == 'False':
                    self.stack.append(False)
                elif value.startswith('"'):
                    self.stack.append(value.strip('"'))
                else:
                    self.stack.append(int(value))
                self.pc += 1
            elif op == 'STORE':
                var = parts[1]
                self.memory[var] = self.stack.pop()
                self.pc += 1
            elif op == 'LOAD':
                var = parts[1]
                self.stack.append(self.memory[var])
                self.pc += 1
            elif op == 'ADD':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                self.pc += 1
            elif op == 'SUB':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                self.pc += 1
            elif op == 'MUL':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                self.pc += 1
            elif op == 'DIV':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a // b)
                self.pc += 1
            elif op == 'LT':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)
                self.pc += 1
            elif op == 'GT':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)
                self.pc += 1
            elif op == 'EQ':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
                self.pc += 1
            elif op == 'AND':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a and b)
                self.pc += 1
            elif op == 'OR':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a or b)
                self.pc += 1
            elif op == 'PRINT':
                print(self.stack.pop())
                self.pc += 1
            elif op == 'LABEL':
                self.pc += 1
            elif op == 'GOTO':
                label = parts[1]
                self.pc = self.labels[label]
            elif op == 'JZ':
                label = parts[1]
                if not self.stack.pop():
                    self.pc = self.labels[label]
                else:
                    self.pc += 1
            else:
                raise Exception(f"Unknown instruction: {instruction}")
