from genLexer import make_lexer
from regex_primitives import *


# =============================================================================|
class EOF:
    def __repr__(self):
        return f"Token({type(self).__name__})"
# =============================================================================|


# =============================================================================|
class Token:
    """

    """

    # -------------------------------------------------------------------------|
    def __init__(self, lexeme):
        """
        Constructor for Token
        """
        self.lexeme = lexeme
    # -------------------------------------------------------------------------|

    # -------------------------------------------------------------------------|
    def __repr__(self):
        """

        """
        return f"Token({type(self).__name__} {self.lexeme})"
    # -------------------------------------------------------------------------|
# =============================================================================|


class LET(Token): pass


class IN(Token): pass


class EQ(Token): pass


class COMMA(Token): pass


class PLUS(Token): pass


class MINUS(Token): pass


class STAR(Token): pass


class SLASH(Token): pass


class INT(Token): pass


class ID(Token): pass


class ARROW(Token): pass


# =============================================================================|
class LexerSpecification:
    """

    """

    # -------------------------------------------------------------------------|
    def __init__(self):
        """
        Constructor for LexerSpecification
        """
        self.eof = EOF()
        self.binding_list = {
            "whitespace": Range(Char(chr(0)), Char(chr(32))),
            "lower": Range(Char("a"), Char("z")),
            "upper": Range(Char("A"), Char("Z")),
            "letter": Or(Name("lower"), Name("upper")),
            "digit": Range(Char("0"), Char("9")),
            "idfirst": Or(Name("letter"), Or(Char("_"), Char("$"))),
            "idrest": Or(Name("idfirst"), Name("digit")),
            "ident": Sequence(Name("idfirst"), Star(Name("idrest"))),
            "digits": Plus(Name("digit")),
            "double": Sequence(r1 = Sequence(r1 = Name("digits"),
                                             r2 = Optional(
                                                 Sequence(r1 = Char("."),
                                                          r2 = Name("digits")))),
                               r2 = Optional(
                                   Sequence(r1 = Or(r1 = Char("E"),
                                                    r2 = Char("e")),
                                            r2 = Sequence(r1 = Optional(
                                                                Or(r1 = Char("E"),
                                                                    r2 = Char("e"))))))))
        }
        self.patterns = [
            (Plus(Name("whitespace")), False),
            ("let", LET),
            ("in", IN),
            ("=", EQ),
            (",", COMMA),
            ("+", PLUS),
            ("-", MINUS),
            ("*", STAR),
            ("/", SLASH),
            ("->", ARROW),
            (Name("letters"), ID),
            (Name("digits"), INT),
        ]
    # -------------------------------------------------------------------------|


# =============================================================================|

# -----------------------------------------------------------------------------|
def main():
    """

    """

    string = "2*3=4 -> 10"
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)
    print(tokens)
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()

