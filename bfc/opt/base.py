# This is a part of Esotope Brainfuck Compiler.

class Transformer(object):
    def __init__(self, target):
        assert isinstance(target, list)
        self.target = target
        self.cursormin = 0
        self.cursormax = 0

    def __iter__(self):
        return self

    def next(self):
        if self.cursormax >= len(self.target):
            raise StopIteration
        self.cursormin = self.cursormax
        self.cursormax += 1
        return self.cursormin, self.target[self.cursormin]

    def prepend(self, *items):
        self.target[self.cursormin:self.cursormin] = items
        self.cursormax += len(items)

    def append(self, *items):
        self.target[self.cursormax:self.cursormax] = items
        self.cursormax += len(items)

    def replace(self, *items):
        self.target[self.cursormin:self.cursormax] = items
        nitems = len(items)
        self.cursormax = self.cursormin + nitems

    def truncate(self):
        del self.target[self.cursormax:]

class BaseOptimizerPass(object):
    def __init__(self, compiler):
        self.compiler = compiler

    def __getattr__(self, name):
        return getattr(self.compiler, name)

    def check(self, node):
        return False

    def transform(self, node):
        return node

