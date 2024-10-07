class Node:
    def __init__(self):
        raise NotImplementedError()
    def __repr__(self):
        selfdict = {i: getattr(self, i) for i in dir(self) if not (i.startswith("__") and i.endswith("__"))}
        attrs = ", ".join(map(lambda x: f"{x[0]}={repr(x[1])}", selfdict.items()))
        return f"{self.__class__.__name__}({attrs})"

class NodeList(Node):
    def __init__(self, args):
        self.args = args
class NodeConst(Node):
    def __init__(self, value):
        self.value = value
class NodeIden(Node):
    def __init__(self, iden):
        self.iden = iden
class NodeAttr(Node):
    def __init__(self, expr, attr):
        self.expr = expr
        self.attr = attr