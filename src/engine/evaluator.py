from itertools import chain
from typing import MutableMapping, List, Set, Tuple

from src.engine.indexed_relation import IndexedRelation
from src.meta.atom import Atom
from src.meta.rule import Rule


class Evaluator:
    def __init__(self, rule: Rule, relations: MutableMapping[str, IndexedRelation]):
        self.rule: Rule = rule

        self.bindings: MutableMapping = dict()
        self.relations = relations

        for atom in chain([rule.head], rule.positive_literals):
            for variable in atom.variables:
                self.bindings[variable.name] = None

        self.bindings.update(rule.initial_bindings)

    def evaluate(self):
        for record in self.lookup_join(self.rule.positive_literals):
            yield from self.filter(record, self.rule.negative_literals)

    def filter(self, record: Tuple[int, ...], atoms: List[Atom]):
        if len(atoms) == 0:
            yield record
        else:
            head, rest = atoms[0], atoms[1:]

            tup = self.prepare_tuple(head)

            if not self.relations.get(head.name).member(tup):
                yield from self.filter(record, rest)

    def lookup_join(self, atoms: List[Atom]):
        if len(atoms) == 0:
            yield self.prepare_tuple(self.rule.head)
        else:
            head, rest = atoms[0], atoms[1:]

            tup = self.prepare_tuple(head)

            rewind_set = self.calculate_rewind_set(head)

            for record in self.relations.get(head.name).lookup(tup):
                if self.bind_tuple(record, head):
                    yield from self.lookup_join(rest)

            self.unbind_tuple(rewind_set)

    def prepare_tuple(self, atom: Atom):
        return tuple(self.bindings[variable.name] for variable in atom.variables)

    def calculate_rewind_set(self, atom):
        rewind_set = set()

        for variable in atom.variables:
            if self.bindings[variable.name]:
                rewind_set.add(variable.name)

        return rewind_set

    def bind_tuple(self, record, atom):
        local_bindings: MutableMapping = dict()

        for value, variable in zip(record, atom.variables):
            if variable.name in local_bindings and local_bindings[variable.name] != value:
                return False
            else:
                local_bindings[variable.name] = value

        self.bindings.update(local_bindings)

        return True

    def unbind_tuple(self, unwind_set: Set[str]):
        for variable in unwind_set:
            self.bindings[variable] = None
