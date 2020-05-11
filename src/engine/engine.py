import os
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
        self.predicates: Mapping[str, int] = {}

        self.variable_id: int = 0

        self.rules: List[Rule] = []

        self._u: Relation[int] = UniverseRelation(-1)

        self.unknown_or_true_facts: Mapping[str, Relation[int]] = {}
        self.true_facts: Mapping[str, Relation[int]] = {}

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
        self.predicates = visitor.predicates

        self._fix_rules()

        self._u = UniverseRelation(len(self.id_to_const) - 1)

        self.unknown_or_true_facts, self.true_facts = Runtime(visitor.rules, self.predicates, self._u).run()

    def _output_rel(self, relation: str, output_dir: str):
        filename = f'{relation}_true.facts'

        with open(os.path.join(output_dir, filename), 'w') as f:
            for record in self.true_facts[relation]:
                f.write(f'{", ".join(tuple(map(lambda y: self.id_to_const[y], record)))}\n')

        filename = f'{relation}_unknown.facts'

        with open(os.path.join(output_dir, filename), 'w') as f:
            for record in self.unknown_or_true_facts[relation]:
                if not self.true_facts[relation].member(record):
                    f.write(f'{", ".join(tuple(map(lambda y: self.id_to_const[y], record)))}\n')

    def output_all(self, output_dir):
        for relation in self.true_facts:
            if not relation == '_U':
                self._output_rel(relation, output_dir)

    def print_all(self):
        print("True")

        for i, q_i in self.true_facts.items():
            if not i == '_U':
                print(f'{i}:', *(tuple(map(lambda y: self.id_to_const[y], x)) for x in q_i))

        print()
        print()

        print("Unknown")

        for i, p_i in self.unknown_or_true_facts.items():
            if not i == '_U':
                print(f'{i}:', *(tuple(map(lambda y: self.id_to_const[y], x)) for x in p_i if not self.true_facts[i].member(x)))
