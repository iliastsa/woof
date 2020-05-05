from typing import Set, MutableMapping

from src.engine.indexed_relation import IndexedRelation


class Evaluator:
    def __init__(self, variables: Set):
        self.variables: Set = variables

        self.bindings: MutableMapping = dict([(var, None) for var in variables])

    def