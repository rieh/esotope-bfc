# This is a part of Esotope Brainfuck Compiler.

from bfc.nodes import *
from bfc.expr import *
from bfc.cond import *

from bfc.opt import flatten, initialmemory, propagate, removedead, simpleloop, stdlib

class Compiler(object):
    """Compiler class.
    
    It connects parser, optimizer passes and code generator into single
    interface, and provides a shared configuration namespace. If you are not
    interested in the internal workings, this class should be sufficient.
    """

    def __init__(self, parser, codegen, cellsize=8, debugging=False):
        """Compiler(parser, codegen, cellsize=8, debugging=False) -> Compiler object

        Creates Compiler object with given Brainfuck environment. parser and
        codegen should be the class subclassed from (respectively) BaseParser and
        BaseGenerator class. cellsize should be 8 (default), 16 or 32. debugging
        can be set to True in order to generate more verbose output."""

        self.cellsize = cellsize
        self.parser = parser
        self.optpasses = [
            flatten.FlattenPass,
            simpleloop.SimpleLoopPass,
            initialmemory.InitialMemoryPass,
            propagate.PropagatePass,
            simpleloop.SimpleLoopPass,
            propagate.PropagatePass,
            removedead.RemoveDeadPass,
            stdlib.StdlibPass,
        ]
        self.codegen = codegen
        self.debugging = debugging

    def parse(self, fp):
        parser = self.parser(self)
        return parser.parse(fp)

    def visit(self, node, func):
        """compiler.visit(node, func) -> anything

        It calls given function with all nodes within given node recursively,
        in the reverse order of depth-first search. (i.e. visit children first
        and visit root later)
        """

        visit = self.visit
        for inode in node:
            if isinstance(inode, ComplexNode): visit(inode, func)
        return func(node)

    def optimize(self, node):
        """compiler.optimize(node) -> node

        Optimizes the given node using internal optimizer passes. You can
        provide additional passes by appending the class to compiler.optpasses.
        The node could be modified in-place.
        """

        for passcls in self.optpasses:
            passobj = passcls(self)
            # TODO passobj.check is not used yet.
            node = passobj.transform(node)
        return node

    def generate(self, node):
        """compiler.generate(node) -> Generator

        Creates the instance of current code generator, and feeds the given node
        to that generator. (It calls flush method so normally everything is
        printed out. Returns the new code generator object."""

        gen = self.codegen(self)
        gen.generate(node)
        gen.flush()
        return gen

    def compile(self, fp):
        """compiler.compile(filelike) -> Generator

        One-shot shortcut for parse, optimization and code generation. It reads
        the source code, optimizes it and generates the output via the current
        code generator."""

        node = self.parse(fp)
        node = self.optimize(node)
        return self.generate(node)

