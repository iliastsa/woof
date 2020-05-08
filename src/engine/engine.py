from antlr4 import InputStream

from src.engine.runtime import Runtime
from src.parser.RuleVisitor import RuleVisitor
from src.parser.antlr.DatalogLexer import DatalogLexer, CommonTokenStream
from src.parser.antlr.DatalogParser import DatalogParser


class Engine:
    def __init__(self, stream: InputStream):
        self.stream: InputStream = stream

    def run(self):
        lexer = DatalogLexer(self.stream)
        parser = DatalogParser(CommonTokenStream(lexer))
        tree = parser.datalogMain()

        visitor = RuleVisitor()
        visitor.visit(tree)

        # TODO: Find which variables are either in the head and are not bound by a body rule or variables that are not
        #       bound by at least one positive literal. Insert a special literal U for each of these variables.
        #       This U\1 predicate contains all the atoms in the program (Herbrand Universe).
        p, q = Runtime(visitor.rules).run()

        return p, q