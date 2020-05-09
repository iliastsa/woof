class ArityException(Exception):
    def __init__(self, conflict):
        self.conflict = conflict

    def __str__(self):
        return f'Mismatched arity at line {self.conflict[0]}, column {self.conflict[1]}: {self.conflict[2]}'
