from actionFunctions import SumInt, DifferenceInt, ProductInt, QuotientInt,\
    Negative
from genLexer import make_lexer
from genParser import make_parser
from lexer import EOF, PLUS, MINUS, STAR, SLASH, INT, ID, OP, CP,\
    LexerSpecification


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


# ----------------------------- #
# - Action-functions -#
# ----------------------------- #
def ignore_eof(expr, eof): return expr


def make_sum(x, sign, y): return SumInt(x, y)


def make_diff(x, sign, y): return DifferenceInt(x, y)


def make_prod(x, sign, y): return ProductInt(x, y)


def make_div(x, sign, y): return QuotientInt(x, y)


def make_neg(sign, x): return Negative(x)


def make_parenthesis(op, x, cp): return x


# =============================================================================|
class Action:
    """

    """

    # -------------------------------------------------------------------------|
    def __init__(self, args_len, action = None):
        """
        Constructor for Action
        """
        self.args_len = args_len
        self.action = action
    # -------------------------------------------------------------------------|

    # -------------------------------------------------------------------------|

    def __repr__(self):
        """

        """
        return f"Action({self.args_len}, {self.action})"
    # -------------------------------------------------------------------------|
# =============================================================================|


# ----------------------------- #

actions = {
    "S": [
        Action(2, ignore_eof),
    ],
    "E":[
        Action(2),
    ],
    "E2":[
        Action(3, make_sum),
        Action(3, make_diff),
        Action(0)
    ],
    "T":[
        Action(2),
    ],
    "T2":[
        Action(3, make_prod),
        Action(3, make_div),
        Action(0)
    ],
    "F":[
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

    string = "4 + 5 - 7 + 9"
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)
    parser = make_parser(grammar, actions)
    print(parser(tokens))
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()
