import platform
import os
import sys


if platform.system() == "Windows":
    os.system("")

RED = "\u001b[31m"
RESET = "\u001b[0m"


def error(msg, line=None, exit_code=1):
    print(RED, end='')
    print("Error:", msg)
    if line is not None:
        print("Line:", str(line))
        print(RESET, end='')
        print(get_line_from_file(line, line.src_file))
    print(RESET, end='')
    sys.exit(exit_code)


def get_line_from_file(pos, filename):
    line = ""
    lineno = pos.line
    with open(filename, 'r') as f:
        for i, raw_line in enumerate(f):
            if i == lineno-1:
                line = raw_line

    underline = " " * (pos.col-1)
    underline += "^" + ("~" * (pos.span-1))

    nl = '\n'
    return f"{line}{nl}{RED}{underline}"
