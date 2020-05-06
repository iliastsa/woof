from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    id: int
    name: str

    def __str__(self):
        return self.name
