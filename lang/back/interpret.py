from ..front.nodes import *
from ..front.lexer import Lexer
from ..front.parser import Parser
import os
from pathlib import Path
import importlib.util
import sys

class Context:
    def __init__(self, ctx=None, parent=None):
        self.ctx = ctx or {}
        self.parent = parent
    def get(self, name):
        if name in self.ctx:
            return self.ctx[name]
        if self.parent is not None and self.parent.has(name):
            return self.parent.get(name)
        raise NameError(name)
    def has(self, name):
        return name in self.ctx or (self.parent.has(name) if self.parent is not None else False)

class Tag:
    def __init__(self, tag):
        self.tag = tag
    def __repr__(self):
        return f":{self.tag}"

class ChoseiModule:
    def __init__(self):
        # vvv this is so terrible but okay
        self.import_locations = [Path(os.getcwd()), Path(os.path.dirname(os.path.realpath(__file__))).parent.parent / "std/"]
        
        def _chse_import(vm: ChoseiModule, *args):
            # (import "path to a mod")
            # (import :mod)
            # (import :mod as this)
            assert len(args) in (1, 3), "Expected (import :mod) or (import :mod as name)"
            
            mod = vm.visit(args[0])
            assert isinstance(mod, (Tag, str)), "Module should be :tag or 'string'"
            if isinstance(mod, Tag):
                mod = mod.tag

            mod_name = mod.split(".")[-1]
            if len(args) == 3:
                assert isinstance(args[1], NodeIden) and args[1].iden == "as", "'as' expected"
                assert isinstance(args[2], NodeIden), "Expected an identifier for 'as' name"
                mod_name = args[2].iden
            
            # determine module location
            for loc in vm.import_locations:
                # check for native (python) module
                if (py_mod := loc / ("/".join(mod.split(".")) + ".py")).exists():
                    spec = importlib.util.spec_from_file_location(mod_name, str(py_mod))
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[spec.name] = module 
                    spec.loader.exec_module(module)
                    vm.ctx_stack[-1].ctx[mod_name] = module
                    return
                elif (chosei_mod := loc / ("/".join(mod.split(".")) + ".chse")).exists():
                    src = chosei_mod.open("r").read()
                    tokens = Lexer(src).run()
                    ast = Parser(tokens).run()
                    module = ChoseiModule()
                    module.run(ast)
                    vm.ctx_stack[-1].ctx[mod_name] = module
                    return
            
            raise ImportError(f"Could not find a name for import: {mod}")

        # TODO: move into some sort of constant? add some basic std functionality
        self.globals = Context({
            "import": _chse_import
        })
        self.ctx_stack = []
    
    def run(self, ast: list[Node]):
        self.ctx_stack.append(Context(parent=self.globals))
        for i in ast:
            self.visit(i)
        self.ctx_stack.pop()

    def visit(self, node: Node):
        return getattr(self, "visit_" + node.__class__.__name__, self.no_visitor)(node)
    
    def no_visitor(self, node: Node):
        raise NotImplementedError(f"no impl in chsemodule for {node}")
    
    def visit_NodeList(self, node: NodeList):
        if len(node.args) == 0:
            return tuple()
        return self.visit(node.args[0])(self, *node.args[1:])
    
    def visit_NodeIden(self, node: NodeIden):
        return self.ctx_stack[-1].get(node.iden)

    def visit_NodeConst(self, node: NodeConst):
        return node.value
    
    def visit_NodeAttr(self, node: NodeAttr):
        return getattr(self.visit(node.expr), node.attr)
    
    def visit_NodeTag(self, node: NodeTag):
        return Tag(node.tag)