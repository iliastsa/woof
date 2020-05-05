from typing import List

from src.meta.predicate import Predicate


class Rule:
    def __init__(self,  head: Predicate, body: List[Predicate]):
        self.head: Predicate = head
        self.body: List[Predicate] = body
