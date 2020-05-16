from sortedcontainers import SortedDict, SortedSet
from typing import Generic, TypeVar, MutableMapping, Tuple, MutableSet, Optional, Generator

from src.engine.relation import Relation

K = TypeVar('K')


class IndexNode(Generic[K]):
    def insert(self, record: Tuple[K, ...]) -> 'IndexNode[K]':
        raise NotImplementedError()

    def contains(self, record: Tuple[K, ...]) -> bool:
        raise NotImplementedError()

    def lookup(self, record: Tuple[Optional[K], ...]) -> Generator[Tuple[K, ...], None, None]:
        raise NotImplementedError()


class InnerNode(Generic[K], IndexNode[K]):
    def __init__(self):
        self.index: MutableMapping[K, IndexNode[K]] = SortedDict()

    def insert(self, record: Tuple[K, ...]) -> 'InnerNode[K]':
        head, rest = record[0], record[1:]

        if len(rest) == 1:
            self.index[head] = self.index.get(head, LeafNode()).insert(rest)
        else:
            self.index[head] = self.index.get(head, InnerNode()).insert(rest)

        return self

    def contains(self, record: Tuple[K, ...]) -> bool:
        head, rest = record[0], record[1:]

        if head in self.index:
            return self.index[head].contains(rest)
        else:
            return False

    def lookup(self, record: Tuple[Optional[K], ...]) -> Generator[Tuple[K, ...], None, None]:
        head, rest = record[0], record[1:]

        if head is not None:
            if head not in self.index:
                self.index[head] = InnerNode() if len(rest) > 1 else LeafNode()

            yield from (((head, ) + x) for x in self.index[head].lookup(rest))
        else:
            for key, value in self.index.items():
                yield from (((key, ) + x) for x in value.lookup(rest))


class LeafNode(Generic[K], IndexNode[K]):
    def __init__(self):
        self.data: MutableSet[K, IndexNode[K]] = SortedSet()

    def insert(self, record: Tuple[K, ...]) -> 'LeafNode[K]':
        self.data.add(record)

        return self

    def contains(self, record: Tuple[K, ...]) -> bool:
        return record in self.data

    def lookup(self, record: Tuple[Optional[K], ...]) -> Generator[Tuple[K, ...], None, None]:
        if record == () or record == (None, ):
            yield from self.data
        elif record in self.data:
            yield record


class IndexedRelation(Relation[K]):
    def __init__(self, arity: int):
        super().__init__(arity)

        self.index_root: IndexNode[K] = LeafNode() if arity <= 1 else InnerNode()

    def lookup(self, record: Tuple[Optional[K], ...]) -> Generator[Tuple[K, ...], None, None]:
        assert len(record) == self.arity

        return self.index_root.lookup(record)

    def member(self, record: Tuple[Optional[K], ...]) -> bool:
        return self.index_root.contains(record)

    def insert(self, record: Tuple[K, ...]) -> None:
        assert len(record) == self.arity

        if self.member(record):
            return

        self.index_root.insert(record)
        self.size += 1

    def copy(self) -> Relation[K]:
        new_rel = IndexedRelation(self.arity)

        for rec in self:
            new_rel.insert(rec)

        return new_rel
