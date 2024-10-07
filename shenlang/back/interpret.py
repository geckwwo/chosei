from ..front.nodes import *

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

class ShenModule:
    def __init__(self):
        def _shen_import(vm, mod):
            # TODO: make this actually usable
            if isinstance(mod, NodeIden):
                mod = mod.iden
            elif isinstance(mod, NodeAttr):
                assert isinstance(mod.expr, NodeIden)
                mod = mod.expr.iden + "." + mod.attr
            else:
                raise ValueError("module has to be iden")
            vm.ctx_stack[-1].ctx[mod.split(".")[-1]] = __import__(mod, fromlist=mod.split("."))
        # TODO: move into some sort of constant? add some basic std functionality
        self.globals = Context({
            "import": _shen_import
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
        raise NotImplementedError(f"no impl in shenmodule for {node}")
    
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