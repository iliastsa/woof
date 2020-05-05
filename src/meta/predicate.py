from dataclasses import dataclass
from typing import Tuple

from src.meta.variable import Variable


@dataclass
class Predicate:
    name: str
    variables: Tuple[Variable, ...]
