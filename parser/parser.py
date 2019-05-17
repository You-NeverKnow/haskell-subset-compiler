from genLexer import make_lexer
from genParser import make_parser
from lexer import EOF, PLUS, MINUS, STAR, SLASH, INT, ID, OP, CP,\
    LexerSpecification

from actions import *

# ---------------------------------------------------- #
# Grammar
# ---------------------------------------------------- #
grammar = {
    "S": [
        ("E", EOF),
    ],
    "E": [
        ("T", "E2"),
    ],
    "E2": [
        (PLUS, "T", "E2"),
        (MINUS, "T", "E2"),
        ()
    ],
    "T": [
        ("F", "T2")
    ],
    "T2": [
        (STAR, "F", "T2"),
        (SLASH, "F", "T2"),
        ()
    ],
    "F": [
        (INT,),
        (ID,),
        (MINUS, "F"),
        (OP, "E", CP),
    ]
}


# ---------------------------------------------------- #
# Actions
# ---------------------------------------------------- #

actions = {
    "S": [
        Action(2, ignore_eof),
    ],
    "E": [
        Action(2),
    ],
    "E2": [
        Action(3, make_sum),
        Action(3, make_diff),
        Action(0)
    ],
    "T": [
        Action(2),
    ],
    "T2": [
        Action(3, make_prod),
        Action(3, make_div),
        Action(0)
    ],
    "F": [
        Action(0),
        Action(0),
        Action(2, make_neg),
        Action(3, make_parenthesis)
    ]
}


# -----------------------------------------------------------------------------|
def main():
    """

    """

    string = "4 + -(5 + 7) - 10 * 0 / 20"
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)
    parser = make_parser(grammar, actions)
    print(parser(tokens))
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()
