class Optimizer:
    def __init__(self, instructions):
        self.instructions = instructions
    
    def optimize(self):
        self.instructions = self.constant_folding()
        self.instructions = self.constant_propagation()
        self.instructions = self.dead_code_elimination()
        return self.instructions
    
    def constant_folding(self):
        optimized = []
        constants = {}
        
        for op, arg1, arg2, result in self.instructions:
            if op == '=' and isinstance(arg1, (int, bool, str)):
                constants[result] = arg1
                optimized.append((op, arg1, arg2, result))
            elif op in ['+', '-', '*', '/', '<', '>', '==', '&&', '||']:
                val1 = constants.get(arg1, arg1)
                val2 = constants.get(arg2, arg2)
                
                if isinstance(val1, int) and isinstance(val2, int):
                    if op == '+':
                        folded = val1 + val2
                    elif op == '-':
                        folded = val1 - val2
                    elif op == '*':
                        folded = val1 * val2
                    elif op == '/':
                        folded = val1 // val2
                    elif op == '<':
                        folded = val1 < val2
                    elif op == '>':
                        folded = val1 > val2
                    elif op == '==':
                        folded = val1 == val2
                    else:
                        optimized.append((op, arg1, arg2, result))
                        continue
                    
                    constants[result] = folded
                    optimized.append(('=', folded, None, result))
                elif isinstance(val1, bool) and isinstance(val2, bool):
                    if op == '&&':
                        folded = val1 and val2
                    elif op == '||':
                        folded = val1 or val2
                    elif op == '==':
                        folded = val1 == val2
                    else:
                        optimized.append((op, arg1, arg2, result))
                        continue
                    
                    constants[result] = folded
                    optimized.append(('=', folded, None, result))
                else:
                    optimized.append((op, arg1, arg2, result))
            else:
                optimized.append((op, arg1, arg2, result))
        
        return optimized
    
    def constant_propagation(self):
        optimized = []
        constants = {}
        
        for op, arg1, arg2, result in self.instructions:
            if op == '=' and isinstance(arg1, (int, bool, str)):
                constants[result] = arg1
            
            new_arg1 = constants.get(arg1, arg1) if arg1 else arg1
            new_arg2 = constants.get(arg2, arg2) if arg2 else arg2
            
            optimized.append((op, new_arg1, new_arg2, result))
        
        return optimized
    
    def dead_code_elimination(self):
        used = set()
        
        for op, arg1, arg2, result in self.instructions:
            if op not in ['=', 'label']:
                if arg1:
                    used.add(arg1)
                if arg2:
                    used.add(arg2)
        
        optimized = []
        for op, arg1, arg2, result in self.instructions:
            if op == '=' and result and result.startswith('t') and result not in used:
                continue
            optimized.append((op, arg1, arg2, result))
        
        return optimized
