import sys

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

# Keywords
class LET(Token): pass
class IN(Token): pass
class CASE(Token): pass
class OF(Token): pass
class IF(Token): pass
class THEN(Token): pass
class ELSE(Token): pass
class BOOL(Token): pass
class ERROR(Token): pass

# Data types
class DATA(Token): pass
class Boolean(Token): pass
class Integer(Token): pass
class Double(Token): pass
class String(Token): pass


# Operators
class EQ(Token): pass
class COMMA(Token): pass

class PLUS(Token): pass
class MINUS(Token): pass
class STAR(Token): pass
class SLASH(Token): pass
class EQ2(Token): pass
class NEQ(Token): pass
class LEQ(Token): pass
class LESS(Token): pass
class GEQ(Token): pass
class GREAT(Token): pass

class PLUSD(Token): pass
class MINUSD(Token): pass
class TIMESD(Token): pass
class DIVIDED(Token): pass
class EQ2D(Token): pass
class NEQD(Token): pass
class LEQD(Token): pass
class LESSD(Token): pass
class GEQD(Token): pass
class GREATD(Token): pass

class LAM(Token): pass
class ARROW(Token): pass
class AND2(Token): pass
class OR2(Token): pass
class OP(Token): pass
class CP(Token): pass
class SEMI(Token): pass
class OB(Token): pass
class CB(Token): pass
class COLON2(Token): pass
class COLON(Token): pass
class UNDER(Token): pass
class AT(Token): pass


# Data
class INT(Token):
    def get_value(self):
        return int(self.lexeme)


class ID(Token): pass


class STR(Token):
    def get_value(self):
        return self.lexeme[1:-1]


class DBL(Token):
    def get_value(self):
        return float(self.lexeme)


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

        double1 = Name("digits")
        double2 = Optional(Sequence(Char("."), Name("digits")))
        double31 = Or(Char("E"), Char("e"))
        double32 = Optional(Or(Char("+"), Char("-")))
        double33 = Name("digits")
        double3 = Optional(Sequence(double31, Sequence(double32, double33)))

        self.binding_list = {
            "whitespace": Range(Char(chr(0)), Char(chr(32))),
            "lower": Range(Char("a"), Char("z")),
            "upper": Range(Char("A"), Char("Z")),
            "letter": Or(Name("lower"), Name("upper")),
            "letters": Plus(Name("letter")),
            "digit": Range(Char("0"), Char("9")),
            "idfirst": Or(Name("letter"), Or(Char("_"), Char("$"))),
            "idrest": Or(Name("idfirst"), Name("digit")),
            "ident": Sequence(Name("idfirst"), Star(Name("idrest"))),
            "digits": Plus(Name("digit")),
            "double": Sequence(double1, Sequence(double2, double3)),
            "string": Sequence(Char('"'),
                               Sequence(Star(Σ_except({'"'})),
                                        Char('"')))
        }
        self.patterns = [
            (Plus(Name("whitespace")), False),
            ("let", LET),
            ("in", IN),

            ("case", CASE),
            ("of", OF),
            ("if", IF),
            ("then", THEN),
            ("else", ELSE),

            ("True", BOOL),
            ("False", BOOL),
            ("error", ERROR),
            ("data", DATA),

            ("Boolean", Boolean),
            ("Integer", Integer),
            ("Double", Double),
            ("String", String),

            ("=", EQ),
            (",", COMMA),
            ("+", PLUS),
            ("-", MINUS),
            ("*", STAR),
            ("/", SLASH),
            ("==", EQ2),
            ("/=", NEQ),
            ("<=", LEQ),
            ("<", LESS),
            (">=", GEQ),
            (">", GREAT),

            ("+.", PLUSD),
            ("-.", MINUSD),
            ("*.", TIMESD),
            ("/.", DIVIDED),
            ("==.", EQ2D),
            ("/=.", NEQD),
            ("<=.", LEQD),
            ("<.", LESSD),
            (">=.", GEQD),
            (">.", GREATD),

            ("\\", LAM),
            ("->", ARROW),
            ("&&", AND2),
            ("||", OR2),
            ("(", OP),
            (")", CP),
            (";", SEMI),
            ("[", OB),
            ("]", CB),
            ("::", COLON2),
            (":", COLON),
            ("_", UNDER),
            ("@", AT),

            (Name("ident"), ID),
            (Name("digits"), INT),
            (Name("string"), STR),
            (Name("double"), DBL),
        ]
    # -------------------------------------------------------------------------|


# =============================================================================|

# -----------------------------------------------------------------------------|
def main():
    """

    """

    filename = sys.argv[1]
    with open(filename) as f:
        string = f.read()
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)

    for token in tokens:
        print(token)
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()

