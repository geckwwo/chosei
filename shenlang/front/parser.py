from .nodes import *
from .tokens import TokenType, Token

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.idx = -1
        self.tok = None

        self.next()
    
    def next(self, step: int = 1):
        self.idx += step
        self.tok = self.tokens[self.idx] if self.idx < len(self.tokens) else None
    
    def run(self):
        root_body = []
        while self.tok.type != TokenType.EOF:
            root_body.append(self.expr())
        return root_body
    
    def expr(self):
        left = self.expr2()
        while self.tok.type == TokenType.DOT:
            self.next()
            left = NodeAttr(left, self.iden().iden)
        return left

    def expr2(self):
        if self.tok.type == TokenType.LPAR:
            return self.list()
        elif self.tok.type in (TokenType.INT, TokenType.FLOAT, TokenType.STR):
            return self.const()
        elif self.tok.type == TokenType.IDEN:
            return self.iden()
        else:
            raise NotImplementedError(self.tok)
    
    def list(self):
        assert self.tok.type == TokenType.LPAR
        self.next()
        args = []
        while self.tok.type != TokenType.RPAR:
            args.append(self.expr())
        self.next()
        return NodeList(args)
    
    def const(self):
        assert self.tok.type in (TokenType.INT, TokenType.FLOAT, TokenType.STR)
        v = NodeConst(self.tok.value)
        self.next()
        return v
    
    def iden(self):
        assert self.tok.type == TokenType.IDEN
        v = NodeIden(self.tok.value)
        self.next()
        return v