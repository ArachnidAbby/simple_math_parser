from math_ast import ASTNode, SrcPosition
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    NUMBER = 0
    KEYWORD = 1
    OPEN_PAREN = 2
    CLOSE_PAREN = 3
    SEMICOLON = 4

    SUM = 10
    SUB = 11
    MUL = 12
    DIV = 13
    EXP = 14
    MOD = 15

    expr = 30
    stmt = 32
    stmtlist = 33

    EOF = -1


@dataclass
class Token:
    typ: TokenType
    value: str | ASTNode
    position: SrcPosition
