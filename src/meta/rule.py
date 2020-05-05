from dataclasses import dataclass
from typing import List, Mapping

from src.meta.atom import Atom


@dataclass
class Rule:
    head: Atom
    positive_literals: List[Atom]

    negative_literals: List[Atom]

    initial_bindings: Mapping[str, int]

    def __str__(self):
        if len(self.positive_literals) == 0:
            return f'{self.head}' + \
                   (' :- ' if self.initial_bindings else '') + \
                   f'{", ".join(f"{var} = {val}" for var, val in self.initial_bindings.items())}.'
        else:
            return f'{self.head} :- {", ".join(str(atom) for atom in self.positive_literals)}' + \
                   (', ' if self.negative_literals else '') + \
                   f'{", ".join(f"!{atom}" for atom in self.negative_literals)}' + \
                   (', ' if self.initial_bindings else '') + \
                   f'{", ".join(f"{var} = {val}" for var, val in self.initial_bindings)}.'
