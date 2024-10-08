import functools as __functools

def add(vm, *args):
    return sum(map(vm.visit, args))
def subtract(vm, *args):
    return __functools.reduce(lambda a, b: a - b, map(vm.visit, args))
def multiply(vm, *args):
    return __functools.reduce(lambda a, b: a * b, map(vm.visit, args))
def divide(vm, *args):
    return __functools.reduce(lambda a, b: a / b, map(vm.visit, args))

globals()["+"] = add
globals()["-"] = subtract
globals()["*"] = multiply
globals()["/"] = divide
globals()["sum"] = add
