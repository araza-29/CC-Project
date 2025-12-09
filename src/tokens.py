from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    LET = auto()
    IF = auto()
    ELSE = auto()
    REPEAT = auto()
    PRINT = auto()
    INT = auto()
    STRING = auto()
    BOOL = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Literals
    NUMBER = auto()
    STRING_LITERAL = auto()
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LT = auto()
    GT = auto()
    EQ = auto()
    AND = auto()
    OR = auto()
    ASSIGN = auto()
    
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    
    # Special
    EOF = auto()

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"
