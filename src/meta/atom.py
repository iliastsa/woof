from dataclasses import dataclass
from typing import Tuple

from src.meta.variable import Variable


@dataclass(frozen=True)
class Atom:
    name: str
    variables: Tuple[Variable, ...]

    def __str__(self):
        return f'{self.name}({", ".join(str(variable) for variable in self.variables)})'
