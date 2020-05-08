from typing import Tuple, Optional, TypeVar, Generator

from src.engine.indexed_relation import IndexedRelation

K = TypeVar('K')


class UniverseRelation(IndexedRelation[K]):
    def __init__(self, max_id: int):
        super(UniverseRelation, self).__init__(1)

        assert -1 <= max_id

        self.size: int = max_id + 1

    def lookup(self, record: Tuple[Optional[K], ...]) -> Generator[Tuple[K, ...]]:
        assert len(record) == 1

        value, = record

        if value is None:
            return range(0, self.size)

        if 0 <= value < self.size:
            yield record

    def member(self, record: Tuple[Optional[K], ...]) -> bool:
        return 0 <= record[0] < self.size

    def insert(self, record: Tuple[K, ...]) -> None:
        pass
