import sys

from genLexer import make_lexer
from regex_primitives import Range, Char, Or, Plus, Name


class EOF: pass


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
            "upper": Range(Char("A"), Char("Z")),
            "lower": Range(Char("a"), Char("z")),
            "letter": Or(Name("lower"), Name("upper")),
            "letters": Plus(Name("letter")),
            "digit": Range(Char("0"), Char("9")),
            "digits": Plus(Name("digit"))
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
            (Name("letters"), ID),
            (Name("digits"), INT),
        ]
    # -------------------------------------------------------------------------|
    
# =============================================================================|


# -----------------------------------------------------------------------------|
def main():
    """

    """

    string = sys.argv[1]
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)
    print(tokens)
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()

