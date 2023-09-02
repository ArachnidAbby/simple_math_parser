from rply import LexerGenerator
from parser_token import TokenType


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Parenthesis
        self.lexer.add(TokenType.OPEN_PAREN, r'\(')
        self.lexer.add(TokenType.CLOSE_PAREN, r'\)')

        # symbols
        self.lexer.add(TokenType.SEMICOLON, r'\;')
        # math
        self.lexer.add(TokenType.SUM, r'\+')
        self.lexer.add(TokenType.SUB, r'\-')
        self.lexer.add(TokenType.MUL, r'\*')
        self.lexer.add(TokenType.DIV, r'\/')
        self.lexer.add(TokenType.EXP, r'\^')
        self.lexer.add(TokenType.MOD, r'\%')

        # Number
        self.lexer.add(TokenType.NUMBER, r'\d+')
        self.lexer.add(TokenType.KEYWORD, r'(\w+)')

        # Ignore spaces
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
