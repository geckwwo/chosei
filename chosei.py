#!/usr/bin/python3
import lang.front.lexer
import lang.front.parser
import lang.back.interpret
import sys

source = open(sys.argv[1]).read()
tokens = lang.front.lexer.Lexer(source).run()
ast = lang.front.parser.Parser(tokens).run()
mod = lang.back.interpret.ChoseiModule()
mod.run(ast)