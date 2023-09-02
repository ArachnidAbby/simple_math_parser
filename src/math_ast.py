from abc import ABC, abstractmethod
from typing import NamedTuple, Self


class SrcPosition(NamedTuple):
    line: int
    col: int
    span: int

    src_file: str

    def __str__(self) -> str:
        return f"{self.src_file}:{self.line}:{self.col}"

    @staticmethod
    def invalid() -> Self:
        return SrcPosition(-1, -1, -1, '')


class ASTNode(ABC):
    def __init__(self, pos: SrcPosition):
        self._pos = pos

    @abstractmethod
    def eval(self, block):
        pass


class Number(ASTNode):
    def __init__(self, pos, val):
        super().__init__(pos)
        self.val = val

    def eval(self, block):
        return self.val

    def __repr__(self) -> str:
        return f"NUMBER-LIT: {self.val}"


class StatementList(ASTNode):
    def __init__(self, pos):
        super().__init__(pos)
        self.children = []

    def append_child(self, child):
        self.children.append(child)
        return self

    def eval(self, block):
        for child in self.children:
            print(f"{child._pos.line}:", child.eval(self))

    def __repr__(self) -> str:
        nl = '\n  '
        raw_nl = "\n"

        inner_str = nl.join([repr(child).replace(raw_nl, nl) for child in self.children])
        return f"STMTLIST: ({nl}{inner_str}{raw_nl})"


class Paren(ASTNode):
    def __init__(self, pos, inner):
        super().__init__(pos)
        self.inner = inner

    def eval(self, block):
        return self.inner.eval(block)

    def __repr__(self) -> str:
        return f"PAREN: {repr(self.inner)}"


class MathNode(ASTNode):
    repr_name = "MATH NODE"

    def __init__(self, pos, lhs, rhs):
        super().__init__(pos)
        self.lhs = lhs
        self.rhs = rhs

    @abstractmethod
    def eval(self, block):
        pass

    def __repr__(self) -> str:
        nl = '\n  '
        raw_nl = "\n"

        lhs_str = repr(self.lhs).replace(raw_nl, nl)
        rhs_str = repr(self.rhs).replace(raw_nl, nl)
        return f"{self.repr_name}: {nl}lhs: ({lhs_str}) {nl}rhs: ({rhs_str}){raw_nl}"


class Sum(MathNode):
    repr_name = "SUM"

    def eval(self, block):
        return self.lhs.eval(block) + self.rhs.eval(block)


class Sub(MathNode):
    repr_name = "SUB"

    def eval(self, block):
        return self.lhs.eval(block) - self.rhs.eval(block)


class Mul(MathNode):
    repr_name = "MUL"

    def eval(self, block):
        return self.lhs.eval(block) * self.rhs.eval(block)


class Div(MathNode):
    repr_name = "DIV"

    def eval(self, block):
        return self.lhs.eval(block) / self.rhs.eval(block)


class Exp(MathNode):
    repr_name = "EXP"

    def eval(self, block):
        return self.lhs.eval(block) ** self.rhs.eval(block)


class Mod(MathNode):
    repr_name = "MOD"

    def eval(self, block):
        return self.lhs.eval(block) % self.rhs.eval(block)