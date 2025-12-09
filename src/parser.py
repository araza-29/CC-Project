from tokens import TokenType
import ast as ast_nodes

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.pos]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type):
        if self.current_token().type != token_type:
            raise Exception(f"Expected {token_type}, got {self.current_token().type}")
        token = self.current_token()
        self.advance()
        return token
    
    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return ast_nodes.Program(statements)
    
    def parse_statement(self):
        token = self.current_token()
        
        if token.type == TokenType.LET:
            return self.parse_let()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.REPEAT:
            return self.parse_repeat()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.IDENTIFIER:
            # Handle assignment (reassignment without 'let')
            return self.parse_assignment()
        else:
            raise Exception(f"Unexpected token: {token}")
    
    def parse_let(self):
        self.expect(TokenType.LET)
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        expression = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ast_nodes.LetStatement(identifier, expression)
    
    def parse_assignment(self):
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        expression = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ast_nodes.LetStatement(identifier, expression)
    
    def parse_if(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        then_block = []
        while self.current_token().type != TokenType.RBRACE:
            then_block.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            else_block = []
            while self.current_token().type != TokenType.RBRACE:
                else_block.append(self.parse_statement())
            self.expect(TokenType.RBRACE)
        
        return ast_nodes.IfStatement(condition, then_block, else_block)
    
    def parse_repeat(self):
        self.expect(TokenType.REPEAT)
        self.expect(TokenType.LPAREN)
        count = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        block = []
        while self.current_token().type != TokenType.RBRACE:
            block.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return ast_nodes.RepeatStatement(count, block)
    
    def parse_print(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expression = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return ast_nodes.PrintStatement(expression)
    
    def parse_expression(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token().type == TokenType.OR:
            op = self.current_token().value
            self.advance()
            right = self.parse_logical_and()
            left = ast_nodes.BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self):
        left = self.parse_comparison()
        while self.current_token().type == TokenType.AND:
            op = self.current_token().value
            self.advance()
            right = self.parse_comparison()
            left = ast_nodes.BinaryOp(left, op, right)
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.current_token().type in [TokenType.LT, TokenType.GT, TokenType.EQ]:
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = ast_nodes.BinaryOp(left, op, right)
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = ast_nodes.BinaryOp(left, op, right)
        return left
    
    def parse_multiplicative(self):
        left = self.parse_primary()
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_primary()
            left = ast_nodes.BinaryOp(left, op, right)
        return left
    
    def parse_primary(self):
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return ast_nodes.Number(token.value)
        elif token.type == TokenType.STRING_LITERAL:
            self.advance()
            return ast_nodes.String(token.value)
        elif token.type == TokenType.TRUE:
            self.advance()
            return ast_nodes.Boolean(True)
        elif token.type == TokenType.FALSE:
            self.advance()
            return ast_nodes.Boolean(False)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return ast_nodes.Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        else:
            raise Exception(f"Unexpected token in expression: {token}")
