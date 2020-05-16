from typing import Tuple, Optional, TypeVar, Generic, Generator

K = TypeVar('K')


class Relation(Generic[K]):
    def __init__(self, arity: int):
        assert arity >= 0

        self.size: int = 0
        self.arity: int = arity

    def lookup(self, record: Tuple[Optional[K], ...]) -> Generator[Tuple[K, ...], None, None]:
        raise NotImplementedError

    def member(self, record: Tuple[Optional[K], ...]) -> bool:
        raise NotImplementedError

    def insert(self, record: Tuple[K, ...]) -> None:
        raise NotImplementedError

    def copy(self) -> 'Relation[K]':
        raise NotImplementedError

    def __str__(self):
        return f'{", ".join(str(x) for x in self)}'

    def __iter__(self):
        return self.lookup((None, ) * self.arity)
