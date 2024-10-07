import string
import enum
from .tokens import Token, TokenType, TOKENTYPES

class LexerMessages(enum.Enum):
    EL00001 = "The string was not terminated."
    EL00002 = "Floating point number contained more than 1 dot."

class LexerMessage(Exception):
    def __init__(self, line: int, rel_pos: int, abs_pos: int, length: int, err_code: str, error: str):
        self.line = line
        self.rel = rel_pos
        self.abs = abs_pos
        self.len = length
        self.code = err_code
        self.reason = error
    @classmethod
    def from_message(cls, message: LexerMessages, line: int, rel_pos: int, abs_pos: int, length: int):
        return LexerMessages(line, rel_pos, abs_pos, length, message.name, message.value)

class Lexer:
    def __init__(self, text: str):
        self.text = text + "\n"

        self.ch = None
        self.abs = -1
        self.rel = 0
        self.line = 1

        self.tokens = []
        
        self.next()

    def next(self, step: int = 1):
        self.abs += step
        self.rel += step
        self.ch = self.text[self.abs] if self.abs < len(self.text) else None
        if self.ch == "\n":
            self.rel = 1
            self.line += 1

    def token(self, token_type, value=None):
        self.tokens.append(Token(self.line, self.rel, self.abs, token_type, value))

    def run(self) -> list[Token]:
        while self.ch is not None:
            if self.ch in TOKENTYPES:
                self.token(TokenType(self.ch))
                self.next()
            elif self.ch in "\t\v\n\r ":
                self.next()
            elif self.ch in "0123456789":
                drel, dabs = self.rel, self.abs
                num = ""
                while self.ch in "0123456789.":
                    num += self.ch
                    self.next()
                if "." in num:
                    self.token(TokenType.INT, int(num))
                else:
                    try:
                        self.token(TokenType.FLOAT, float(num))
                    except ValueError:
                        raise LexerMessage.from_message(LexerMessages.EL00002, self.line, drel, dabs, len(num))
            elif self.ch in "\"'":
                drel, dabs, quote = self.rel, self.abs, self.ch
                self.next()
                s = ""
                while True:
                    if self.ch is None or self.ch == "\n":
                        raise LexerMessage.from_message(LexerMessages.EL00001, self.line, drel, dabs, len(s) + 1)
                    if self.ch == quote:
                        self.next()
                        break
                    s += self.ch
                    self.next()
                self.token(TokenType.STR, s)
            elif self.ch == ":":
                self.next()
                tag = ""
                while self.ch not in "".join(filter(lambda x: isinstance(x, str), TOKENTYPES)) + "\t\v\n\r :":
                    tag += self.ch
                    self.next()
                self.token(TokenType.TAG, tag)
            else:
                iden = ""
                while self.ch not in "".join(filter(lambda x: isinstance(x, str), TOKENTYPES)) + "\t\v\n\r :":
                    iden += self.ch
                    self.next()
                self.token(TokenType.IDEN, iden)

        self.token(TokenType.EOF)
        return self.tokens