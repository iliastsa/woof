from itertools import chain
from typing import MutableMapping, List, Set

from src.engine.indexed_relation import IndexedRelation
from src.meta.atom import Atom
from src.meta.rule import Rule


class Evaluator:
    def __init__(self, rule: Rule, initial_bindings: MutableMapping, relations: MutableMapping[str, IndexedRelation]):
        self.rule: Rule = rule

        self.bindings: MutableMapping = dict()
        self.relations = relations

        for predicate in chain([rule.head], rule.body):
            for variable in predicate.variables:
                self.bindings[variable.name] = None

        self.bindings.update(initial_bindings)

    def evaluate(self):
        return self.lookup_join(self.rule.body)

    def lookup_join(self, predicates: List[Atom]):
        if len(predicates) == 0:
            yield self.prepare_tuple(self.rule.head)
        else:
            head, rest = predicates[0], predicates[1:]

            tup = self.prepare_tuple(head)

            rewind_set = self.calculate_rewind_set(head)

            for record in self.relations.get(head.name).lookup(tup):
                if self.bind_tuple(record, head):
                    yield from self.lookup_join(rest)

            self.unbind_tuple(rewind_set)

    def prepare_tuple(self, predicate: Atom):
        return tuple(self.bindings[variable.name] for variable in predicate.variables)

    def calculate_rewind_set(self, predicate):
        rewind_set = set()

        for variable in predicate.variables:
            if variable.name not in self.bindings:
                rewind_set.add(variable.name)

        return rewind_set

    def bind_tuple(self, record, predicate):
        local_bindings: MutableMapping = dict()

        for value, variable in zip(record, predicate.variables):
            if variable.name in local_bindings and local_bindings[variable.name] != value:
                return False
            else:
                local_bindings[variable.name] = value

        self.bindings.update(local_bindings)

        return True

    def unbind_tuple(self, unwind_set: Set[str]):
        for variable in unwind_set:
            self.bindings[variable] = None
