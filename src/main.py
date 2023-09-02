import math_lexer
import math_ast
import parser_token
import math_parser


def lex(file):
    with open(file, 'r') as f:
        contents = f.read()

    lexer = math_lexer.Lexer().get_lexer()

    raw_tokens = lexer.lex(contents)
    tokens = []
    for tok in raw_tokens:
        pos = math_ast.SrcPosition(
            tok.source_pos.lineno,
            tok.source_pos.colno,
            len(tok.value),
            file
        )

        tokens.append(
            parser_token.Token(tok.name, tok.value, pos)
        )

    return tokens


if __name__ == "__main__":
    FILE = "testfile.math"

    tokens = lex(FILE)
    # print(tokens)

    parser = math_parser.Parser(tokens)

    parser.parse()

    print('\n'.join([f"{_.typ} "+repr(_.value) for _ in parser.tokens]))

    print("\n\nEVALUATING")
    print("-"*16, '\n\n')
    for token in parser.tokens:
        token.value.eval(None)
