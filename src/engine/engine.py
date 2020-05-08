from collections import Mapping
from itertools import chain
from typing import List

from antlr4 import InputStream

from src.engine.relation import Relation
from src.engine.runtime import Runtime
from src.engine.universe_relation import UniverseRelation
from src.meta.atom import Atom
from src.meta.rule import Rule
from src.meta.variable import Variable
from src.parser.RuleVisitor import RuleVisitor
from src.parser.antlr.DatalogLexer import DatalogLexer, CommonTokenStream
from src.parser.antlr.DatalogParser import DatalogParser


class Engine:
    def __init__(self, stream: InputStream):
        self.stream: InputStream = stream
        self.id_to_const: Mapping[int, str] = {}

        self.variable_id: int = 0

        self.rules: List[Rule] = []

        self._u: Relation[int] = UniverseRelation(-1)

        self.p: Mapping[int, Relation[int]] = {}
        self.q: Mapping[int, Relation[int]] = {}

    def _fix_rules(self):
        for rule in self.rules:
            positive_variables = set()
            for literal in rule.positive_literals:
                positive_variables.update(variable.name for variable in literal.variables)

            negative_variables = set()
            for literal in rule.negative_literals:
                negative_variables.update(variable.name for variable in literal.variables)

            head_variables = set(variable.name for variable in rule.head.variables)

            body_variables = set(chain(negative_variables, positive_variables))

            dangling_variables = set()
            for variable in head_variables:
                if variable not in body_variables and variable not in rule.initial_bindings.keys():
                    dangling_variables.add(variable)

            for variable in negative_variables:
                if variable not in positive_variables and variable not in rule.initial_bindings.keys():
                    dangling_variables.add(variable)

            for variable in dangling_variables:
                rule.positive_literals.append(Atom('_U', (Variable(self.variable_id, variable), )))
                self.variable_id += 1

    def run(self):
        lexer = DatalogLexer(self.stream)
        parser = DatalogParser(CommonTokenStream(lexer))
        tree = parser.datalogMain()

        visitor = RuleVisitor()
        visitor.visit(tree)

        self.rules = visitor.rules
        self.variable_id = visitor.variable_id
        self.id_to_const = visitor.id_to_str

        self._fix_rules()

        self._u = UniverseRelation(len(self.id_to_const) - 1)

        self.p, self.q = Runtime(visitor.rules, self._u).run()

        return self.p, self.q