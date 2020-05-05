from dataclasses import dataclass


@dataclass
class Variable:
    id: int
    name: str

    def __str__(self):
        return self.name
