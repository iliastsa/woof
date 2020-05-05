from typing import List, MutableMapping

from src.meta.atom import Atom
from src.meta.variable import Variable
from src.parser.antlr.DatalogVisitor import DatalogVisitor
from src.parser.antlr.DatalogParser import DatalogParser
from src.meta.rule import Rule


class RuleVisitor(DatalogVisitor):
    def __init__(self):
        self.rules: List[Rule] = []

        self.str_to_id: MutableMapping[str, int] = {}
        self.id_to_str: MutableMapping[int, str] = {}

        self.variable_id = 0
        self.constant_counter = 0

        self.initial_bindings = {}

        self.head = None

        self.p_literals = []
        self.n_literals = []

        self.vars = []

    def visitMRule(self, ctx: DatalogParser.MRuleContext):
        self.reset_rule_state()

        if ctx.body:
            self.visit(ctx.body)

        self.rules.append(Rule(self.visit(ctx.head), self.p_literals, self.n_literals, self.initial_bindings))

    def visitConst(self, ctx: DatalogParser.ConstContext):
        var_id, var_name = self.variable_id, f'v{self.variable_id}'
        self.variable_id += 1

        self.vars.append(Variable(var_id, var_name))

        const_id = self.add_constant(ctx.value)
        self.initial_bindings[var_name] = const_id

    def visitVariable(self, ctx: DatalogParser.VariableContext):
        var_id, var_name = self.variable_id, ctx.name.text
        self.variable_id += 1

        self.vars.append(Variable(var_id, var_name))

    def visitAtom(self, ctx: DatalogParser.AtomContext):
        self.reset_atom_state()

        self.visitTermList(ctx.terms)

        return Atom(ctx.name.text, tuple(self.vars))

    def visitLiteralAtom(self, ctx: DatalogParser.LiteralAtomContext):
        self.p_literals.append(self.visit(ctx.children[0]))

    def visitLiteralNegAtom(self, ctx: DatalogParser.LiteralNegAtomContext):
        self.n_literals.append(self.visit(ctx.children[1]))

    def reset_atom_state(self):
        self.vars = []

    def reset_rule_state(self):
        self.head = None
        self.initial_bindings = {}
        self.p_literals = []
        self.n_literals = []

    def add_constant(self, constant: str) -> int:
        if constant in self.str_to_id:
            return self.str_to_id[constant]
        else:
            self.str_to_id[constant] = self.constant_counter
            self.id_to_str[self.constant_counter] = constant

            self.constant_counter += 1

            return self.str_to_id[constant]