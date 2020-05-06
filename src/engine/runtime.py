from typing import MutableMapping, List

from src.engine.evaluator import Evaluator
from src.engine.indexed_relation import IndexedRelation
from src.meta.rule import Rule


class Runtime:
    def __init__(self, rules: List[Rule]):
        self.P: MutableMapping[str, IndexedRelation] = {}
        self.Q: MutableMapping[str, IndexedRelation] = {}
        self.S: MutableMapping[str, IndexedRelation] = {}

        self.rules = rules

        for head in set(_head for _head in (rule.head for rule in rules)):
            self.P[head.name] = IndexedRelation(len(head.variables))

    def copy_rel(self, inp: IndexedRelation):
        new_rel = IndexedRelation(inp.arity)

        for tup in inp.lookup((None, ) * inp.arity):
            new_rel.insert(tup)

        return new_rel

    def step(self):
        for i, p_i in self.P.items():
            self.Q[i] = self.copy_rel(p_i)
            self.P[i] = IndexedRelation(p_i.arity)

        for rule in self.rules:
            evaluator = Evaluator(rule, self.Q)

            for tup in evaluator.evaluate():
                self.P[rule.head.name].insert(tup)

        for i, p_i in self.P.items():
            self.S[i] = self.copy_rel(p_i)
            self.P[i] = IndexedRelation(p_i.arity)

        for rule in self.rules:
            evaluator = Evaluator(rule, self.S)

            for tup in evaluator.evaluate():
                self.P[rule.head.name].insert(tup)

        for i in range(0):
            pass

    def run(self):
        while True:
            self.step()

            for i in self.P.keys():
                if self.P[i].size != self.Q[i].size:
                    break
            else:
                break

        return self.P, self.S
