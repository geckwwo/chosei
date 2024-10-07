def println(mod, *x):
    print(*(mod.visit(i) for i in x))