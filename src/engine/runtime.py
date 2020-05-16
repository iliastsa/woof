from typing import MutableMapping, List, Mapping

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

        self.universe: Relation = universe
        self.predicates: Mapping[str, int] = predicates
        self.rules: List[Rule] = rules

        for name, arity in predicates.items():
            self.P[name] = IndexedRelation(arity)

    def inner_step(self, edb_relations: Mapping[str, Relation]) -> Mapping[str, Relation]:
        idb_relations: MutableMapping[str, Relation] = {'_U': self.universe}

        for name, arity in self.predicates.items():
            idb_relations[name] = IndexedRelation(arity)

        change = True
        while change:
            change = False

            for rule in self.rules:
                evaluator = Evaluator(rule, idb_relations, edb_relations)

                for rec in evaluator.evaluate():
                    if rec not in idb_relations[rule.head.name]:
                        idb_relations[rule.head.name].insert(rec)

                        change = True

        return idb_relations

    def step(self):
        def copy_and_reset(src: MutableMapping[str, Relation], dest: MutableMapping[str, Relation]):
            for i, rel in src.items():
                if i == '_U':
                    continue

                dest[i] = rel.copy()
                src[i] = IndexedRelation(rel.arity)

        copy_and_reset(self.P, self.Q)

        self.P.update(self.inner_step(self.Q))

        copy_and_reset(self.P, self.S)

        self.P.update(self.inner_step(self.S))

    def run(self):
        while True:
            self.step()

            for i in self.P.keys():
                if self.P[i].size != self.Q[i].size:
                    break
            else:
                break

        return self.P, self.S
