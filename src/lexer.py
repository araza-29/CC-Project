import re
from tokens import Token, TokenType

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.keywords = {
            'let': TokenType.LET,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'repeat': TokenType.REPEAT,
            'print': TokenType.PRINT,
            'int': TokenType.INT,
            'string': TokenType.STRING,
            'bool': TokenType.BOOL,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE
        }
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def read_number(self):
        start_col = self.column
        num = ''
        while self.current_char() and self.current_char().isdigit():
            num += self.current_char()
            self.advance()
        return Token(TokenType.NUMBER, int(num), self.line, start_col)
    
    def read_string(self):
        start_col = self.column
        self.advance()  # skip opening quote
        string = ''
        while self.current_char() and self.current_char() != '"':
            string += self.current_char()
            self.advance()
        self.advance()  # skip closing quote
        return Token(TokenType.STRING_LITERAL, string, self.line, start_col)
    
    def read_identifier(self):
        start_col = self.column
        ident = ''
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, self.line, start_col)
    
    def tokenize(self):
        tokens = []
        
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            ch = self.current_char()
            col = self.column
            
            if ch.isdigit():
                tokens.append(self.read_number())
            elif ch == '"':
                tokens.append(self.read_string())
            elif ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
            elif ch == '+':
                tokens.append(Token(TokenType.PLUS, ch, self.line, col))
                self.advance()
            elif ch == '-':
                tokens.append(Token(TokenType.MINUS, ch, self.line, col))
                self.advance()
            elif ch == '*':
                tokens.append(Token(TokenType.MULTIPLY, ch, self.line, col))
                self.advance()
            elif ch == '/':
                tokens.append(Token(TokenType.DIVIDE, ch, self.line, col))
                self.advance()
            elif ch == '<':
                tokens.append(Token(TokenType.LT, ch, self.line, col))
                self.advance()
            elif ch == '>':
                tokens.append(Token(TokenType.GT, ch, self.line, col))
                self.advance()
            elif ch == '=':
                self.advance()
                if self.current_char() == '=':
                    tokens.append(Token(TokenType.EQ, '==', self.line, col))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.ASSIGN, '=', self.line, col))
            elif ch == '&':
                self.advance()
                if self.current_char() == '&':
                    tokens.append(Token(TokenType.AND, '&&', self.line, col))
                    self.advance()
            elif ch == '|':
                self.advance()
                if self.current_char() == '|':
                    tokens.append(Token(TokenType.OR, '||', self.line, col))
                    self.advance()
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, ch, self.line, col))
                self.advance()
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ch, self.line, col))
                self.advance()
            elif ch == '{':
                tokens.append(Token(TokenType.LBRACE, ch, self.line, col))
                self.advance()
            elif ch == '}':
                tokens.append(Token(TokenType.RBRACE, ch, self.line, col))
                self.advance()
            elif ch == ';':
                tokens.append(Token(TokenType.SEMICOLON, ch, self.line, col))
                self.advance()
            else:
                raise Exception(f"Unknown character: {ch} at {self.line}:{col}")
        
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
