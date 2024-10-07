import enum

class TokenType(enum.Enum):
    EOF = -1

    INT = 1
    FLOAT = 2
    STR = 3
    TAG = 4
    IDEN = 5
    DOT = "."

    LPAR = "("
    RPAR = ")"

TOKENTYPES = list(i.value for i in TokenType)

class Token:
    def __init__(self, line, rel_pos, abs_pos, token_type, value=None):
        self.line = line
        self.rel = rel_pos
        self.abs = abs_pos
        self.type = token_type
        self.value = value
    def __repr__(self):
        return f"<{self.type}" + (f" : {self.value}>" if self.value is not None else ">")