from sortedcontainers import SortedDict, SortedSet
from typing import Generic, TypeVar, MutableMapping, Tuple, MutableSet, Sequence, Optional

K = TypeVar('K')


class IndexNode(Generic[K]):
    def insert(self, record: Tuple[K, ...]) -> 'IndexNode[K]':
        raise NotImplementedError()

    def lookup(self, record: Tuple[Optional[K], ...]) -> Sequence[K]:
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

    def lookup(self, record: Tuple[Optional[K], ...]) -> Sequence[K]:
        head, rest = record[0], record[1:]

        if head is not None:
            yield from (((head, ) + x) for x in self.index.get(head, InnerNode() if len(rest) > 1 else LeafNode()).lookup(rest))
        else:
            for key, value in self.index.items():
                yield from (((key, ) + x) for x in value.lookup(rest))


class LeafNode(Generic[K], IndexNode[K]):
    def __init__(self):
        self.data: MutableSet[K, IndexNode[K]] = SortedSet()

    def insert(self, record: Tuple[K, ...]) -> 'LeafNode[K]':
        self.data.add(record)

        return self

    def lookup(self, record: Tuple[Optional[K], ...]) -> Sequence[K]:
        if record == () or record == (None, ):
            yield from self.data
        elif record in self.data:
            yield record


class IndexedRelation(Generic[K]):
    def __init__(self, arity: int):
        assert arity >= 0

        self.arity: int = arity
        self.size:  int = 0
        self.index_root: IndexNode[K] = LeafNode() if arity <= 1 else InnerNode()

    def lookup(self, record: Tuple[Optional[K], ...]):
        assert len(record) == self.arity

        return self.index_root.lookup(record)

    def member(self, record: Tuple[Optional[K], ...]) -> bool:
        return record in self.lookup(record)

    def insert(self, record: Tuple[K, ...]):
        assert len(record) == self.arity

        if self.member(record):
            return

        self.index_root.insert(record)
        self.size += 1
