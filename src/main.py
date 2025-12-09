import sys
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator
from optimizer import Optimizer
from codegen import CodeGenerator
from vm import VirtualMachine

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.miniflow>")
        return
    
    filename = sys.argv[1]
    
    with open(filename, 'r') as f:
        source = f.read()
    
    # Lexical Analysis
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic Analysis
    semantic = SemanticAnalyzer()
    semantic.analyze(ast)
    
    # TAC Generation
    tac_gen = TACGenerator()
    tac = tac_gen.generate(ast)
    
    # Optimization
    optimizer = Optimizer(tac)
    optimized_tac = optimizer.optimize()
    
    # Code Generation
    codegen = CodeGenerator(optimized_tac)
    code = codegen.generate()
    
    # Execute
    vm = VirtualMachine(code)
    vm.run()

if __name__ == '__main__':
    main()
