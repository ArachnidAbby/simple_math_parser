import errors
from math_ast import (Div, Exp, Mod, Mul, Number, Paren, SrcPosition, StatementList,
                      Sub, Sum)
from parser_token import Token, TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def peek(self, ind: int) -> Token:
        if ind >= len(self.tokens) or ind < 0:
            return Token(TokenType.EOF, '', SrcPosition.invalid())

        return self.tokens[ind]

    def generic_check(self, ind: int):
        if isinstance(self.peek(ind).value, str):
            errors.error("Syntax Error!", line=self.peek(ind).position)

    def parse(self, start=0, min_match=0):
        if self.peek(start).typ == TokenType.EOF:
            return

        self.parse_numbers(start, min_match)
        self.parse_neg(start, min_match)
        self.parse_parens(start, min_match)
        self.parse_sum(start, min_match)
        self.parse_sub(start, min_match)
        self.parse_mul(start, min_match)
        self.parse_div(start, min_match)
        self.parse_mod(start, min_match)
        self.parse_exp(start, min_match)
        self.parse_stmt(start, min_match)
        self.parse_stmtlist_start(start, min_match)
        self.parse_stmtlist_continue(start, min_match)

    def parse_numbers(self, start, min_match):
        if self.peek(start).typ != TokenType.NUMBER:
            return

        val = int(self.peek(start).value)  # type: ignore
        pos = self.peek(start).position
        self.tokens[start] = Token(TokenType.expr, Number(pos, val), pos)

        self.parse(start, min_match)

    def parse_neg(self, start, min_match):
        if self.peek(start-1).typ == TokenType.expr:
            return
        if self.peek(start).typ != TokenType.SUB:
            return
        if self.peek(start+1).typ != TokenType.NUMBER:
            return

        val = -1 * int(self.peek(start+1).value)  # type: ignore
        pos = self.peek(start).position
        del self.tokens[start+1]
        self.tokens[start] = Token(TokenType.expr, Number(pos, val), pos)

        self.parse(start, min_match)

    def parse_parens(self, start, min_match):
        if self.peek(start).typ != TokenType.OPEN_PAREN:
            return

        self.parse(start+1, 0)
        self.generic_check(start+1)

        if self.peek(start+1).typ != TokenType.expr:
            return
        if self.peek(start+2).typ != TokenType.CLOSE_PAREN:
            return

        pos = self.peek(start).position
        val = Paren(pos, self.peek(start+1).value)
        del self.tokens[start+1]
        del self.tokens[start+1]

        self.tokens[start] = Token(TokenType.expr, val, pos)

        self.parse(start, min_match)

    def parse_sum(self, start, min_match):
        if min_match > 1:
            return

        if self.peek(start).typ != TokenType.expr:
            return
        if self.peek(start+1).typ != TokenType.SUM:
            return

        self.parse(start+2, 2)
        self.generic_check(start+2)

        if self.peek(start+2).typ != TokenType.expr:
            return

        lhs = self.peek(start).value
        rhs = self.peek(start+2).value
        pos = self.peek(start).position
        del self.tokens[start+1]
        del self.tokens[start+1]

        sum = Sum(pos, lhs, rhs)
        self.tokens[start] = Token(TokenType.expr, sum, pos)

        self.parse(start, min_match)

    def parse_sub(self, start, min_match):
        if min_match > 1:
            return

        if self.peek(start).typ != TokenType.expr:
            return
        if self.peek(start+1).typ != TokenType.SUB:
            return

        self.parse(start+2, 2)
        self.generic_check(start+2)

        if self.peek(start+2).typ != TokenType.expr:
            return

        lhs = self.peek(start).value
        rhs = self.peek(start+2).value
        pos = self.peek(start).position

        del self.tokens[start+1]
        del self.tokens[start+1]

        sub = Sub(pos, lhs, rhs)
        self.tokens[start] = Token(TokenType.expr, sub, pos)

        self.parse(start, min_match)

    def parse_mul(self, start, min_match):
        if min_match > 2:
            return

        if self.peek(start).typ != TokenType.expr:
            return
        if self.peek(start+1).typ != TokenType.MUL:
            return

        self.parse(start+2, 3)
        self.generic_check(start+2)

        if self.peek(start+2).typ != TokenType.expr:
            return

        lhs = self.peek(start).value
        rhs = self.peek(start+2).value
        pos = self.peek(start).position
        del self.tokens[start+1]
        del self.tokens[start+1]

        mul = Mul(pos, lhs, rhs)
        self.tokens[start] = Token(TokenType.expr, mul, pos)

        self.parse(start, min_match)

    def parse_div(self, start, min_match):
        if min_match > 2:
            return

        if self.peek(start).typ != TokenType.expr:
            return
        if self.peek(start+1).typ != TokenType.DIV:
            return

        self.parse(start+2, 3)
        self.generic_check(start+2)

        if self.peek(start+2).typ != TokenType.expr:
            return

        lhs = self.peek(start).value
        rhs = self.peek(start+2).value
        pos = self.peek(start).position

        del self.tokens[start+1]
        del self.tokens[start+1]

        div = Div(pos, lhs, rhs)
        self.tokens[start] = Token(TokenType.expr, div, pos)

        self.parse(start, min_match)

    def parse_mod(self, start, min_match):
        if min_match > 2:
            return

        if self.peek(start).typ != TokenType.expr:
            return
        if self.peek(start+1).typ != TokenType.MOD:
            return

        self.parse(start+2, 3)
        self.generic_check(start+2)

        if self.peek(start+2).typ != TokenType.expr:
            return

        lhs = self.peek(start).value
        rhs = self.peek(start+2).value
        pos = self.peek(start).position

        del self.tokens[start+1]
        del self.tokens[start+1]

        mod = Mod(pos, lhs, rhs)
        self.tokens[start] = Token(TokenType.expr, mod, pos)

        self.parse(start, min_match)

    def parse_exp(self, start, min_match):
        if min_match > 3:
            return

        if self.peek(start).typ != TokenType.expr:
            return
        if self.peek(start+1).typ != TokenType.EXP:
            return

        self.parse(start+2, 3)
        self.generic_check(start+2)

        if self.peek(start+2).typ != TokenType.expr:
            return

        lhs = self.peek(start).value
        rhs = self.peek(start+2).value
        pos = self.peek(start).position

        del self.tokens[start+1]
        del self.tokens[start+1]

        exp = Exp(pos, lhs, rhs)
        self.tokens[start] = Token(TokenType.expr, exp, pos)

        self.parse(start, min_match)

    def parse_stmt(self, start, min_match):
        if min_match > 1:
            return

        if self.peek(start).typ != TokenType.expr:
            return

        if self.peek(start+1).typ != TokenType.SEMICOLON:
            return

        del self.tokens[start+1]

        self.tokens[start].typ = TokenType.stmt

        self.parse(start, min_match)

    def parse_stmtlist_start(self, start, min_match):
        if min_match > 0:
            return

        if self.peek(start).typ != TokenType.stmt:
            return

        self.parse(start+1, 1)

        if self.peek(start+1).typ != TokenType.stmt:
            return

        stmt2 = self.peek(start+1)
        stmt = self.peek(start)

        del self.tokens[start+1]

        stmtlist = StatementList(stmt.position)
        stmtlist.append_child(stmt.value)\
                .append_child(stmt2.value)

        self.tokens[start] = Token(TokenType.stmtlist, stmtlist, stmt.position)
        self.parse(start, 0)

    def parse_stmtlist_continue(self, start, min_match):
        if min_match > 0:
            return

        if self.peek(start).typ != TokenType.stmtlist:
            return

        self.parse(start+1, 1)

        if self.peek(start+1).typ == TokenType.stmtlist:
            stmtlist = self.peek(start).value
            stmtlist2 = self.peek(start).value
            del self.tokens[start+1]
            stmtlist.children += stmtlist2.children  # type: ignore
            self.parse(start, 0)
            return

        if self.peek(start+1).typ != TokenType.stmt:
            return

        stmtlist = self.peek(start).value
        stmt = self.peek(start+1).value
        del self.tokens[start+1]
        stmtlist.append_child(stmt)
        self.parse(start, 0)
