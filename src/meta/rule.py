from dataclasses import dataclass
from typing import List

from src.meta.predicate import Predicate


@dataclass
class Rule:
    head: Predicate
    body: List[Predicate]
