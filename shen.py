#!/usr/bin/python3
import shenlang.front.lexer
import shenlang.front.parser
import shenlang.back.interpret
import sys

source = open(sys.argv[1]).read()
tokens = shenlang.front.lexer.Lexer(source).run()
ast = shenlang.front.parser.Parser(tokens).run()
mod = shenlang.back.interpret.ShenModule()
mod.run(ast)