from typing import MutableMapping, List, Mapping, Set

from src.engine.evaluator import Evaluator
from src.engine.indexed_relation import IndexedRelation
from src.engine.relation import Relation
from src.engine.universe_relation import UniverseRelation
from src.meta.rule import Rule


class Runtime:
    def __init__(self, rules: List[Rule], predicates: Mapping[str, int], universe: UniverseRelation):
        self.P: MutableMapping[str, Relation] = {'_U': universe}
        self.Q: MutableMapping[str, Relation] = {'_U': universe}
        self.S: MutableMapping[str, Relation] = {'_U': universe}

        self.rules = rules

        for name, arity in predicates.items():
            self.P[name] = IndexedRelation(arity)

    def step(self):
        def copy_rel(inp: Relation):
            if isinstance(inp, UniverseRelation):
                return inp

            new_rel = IndexedRelation(inp.arity)

            for rec in inp.lookup((None,) * inp.arity):
                new_rel.insert(rec)

            return new_rel

        for i, p_i in self.P.items():
            if i == '_U':
                continue

            self.Q[i] = copy_rel(p_i)
            self.P[i] = IndexedRelation(p_i.arity)

        for rule in self.rules:
            evaluator = Evaluator(rule, self.Q)

            for tup in evaluator.evaluate():
                self.P[rule.head.name].insert(tup)

        for i, p_i in self.P.items():
            if i == '_U':
                continue

            self.S[i] = copy_rel(p_i)
            self.P[i] = IndexedRelation(p_i.arity)

        for rule in self.rules:
            evaluator = Evaluator(rule, self.S)

            for tup in evaluator.evaluate():
                self.P[rule.head.name].insert(tup)

    def run(self):
        while True:
            self.step()

            for i in self.P.keys():
                if self.P[i].size != self.Q[i].size:
                    break
            else:
                break

        return self.P, self.S
