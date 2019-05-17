from lexer import *

# ---------------------------------------------------- #
# Grammar
# ---------------------------------------------------- #
grammar = {
    "S": [
        ("decls", EOF),
    ],
    "decls": [
        (),
        ("decl", "decls"),
    ],

    # Declarations
    "decl": [
        (DATA, ID, "fmls", EQ, "cstrs"),
        (ID, "decl2")
    ],
    "decl2": [
        (COLON, "type"),
        (EQ, "m"),
        (OP, "ps", CP, "decl3")
    ],
    "decl3": [
        (EQ, "m"),
        (OP, "ps", CP, "decl3")
    ],

    # Formals aka lhs of a declaration
    "fmls": [
        (),
        (ID, "fmls2"),
    ],
    "fmls2": [
        (),
        (COMMA, ID, "fmls2"),
    ],

    # Constructors
    "cstr": [
        (ID, "types"),
    ],
    "cstrs": [
        ("cstr", "cstrs2"),
    ],
    "cstrs2": [
        (),
        (OR2, "cstr", "cstrs2"),
    ],

    # Types
    "type": [
        ("type2", "type3"),
    ],
    "type2": [
        (Boolean, ),
        (Integer, ),
        (Double, ),
        (String, ),
        (ID, "type4"),
        (OP, "types", CP),
        (OB, "type", CB),
    ],
    "type3": [
        (),
        (ARROW, "type"),
    ],
    "type4": [
        (),
        (OP, "types", CP),
    ],
    "types": [
        (),
        ("type", "types2"),
    ],
    "types2": [
        (),
        (COMMA, "type", "types2"),
    ],

    # Sequences ?
    "seq": [
        (),
        ("m", "seq2"),
    ],
    "seq2": [
        (),
        (COMMA, "m", "seq2"),
    ],
    "m": [
        (IF, "m", THEN, "m", ELSE, "m"),
        (CASE, "m", OF, "mbs"),
        (LET, "ds", IN, "m"),
        (LAM, "mbs"),
        (ERROR, "m"),
        ("bo",),
    ],
    "d": [
        ("p", EQ, "m")
    ],
    "ds": [
        ("d", "ds2")
    ],
    "ds2": [
        (),
        (COMMA, "d", "ds2")
    ],

    # Lambda
    "mb": [
        ("p", ARROW, OP, "m", CP),
    ],
    "mbs": [
        ("mb", "mbs2"),
    ],
    "mbs2": [
        (),
        (SEMI, "mb", "mbs2"),
    ],
    "p": [
        ("ap", "p2"),
    ],
    "p2": [
        (),
        (COLON2, "p"),
    ],
    "ap": [
        (BOOL, ),
        (INT, ),
        (DBL, ),
        (MINUS, INT),
        (MINUSD, DBL),
        (STR, ),
        (ID, "ap2"),
        (OB, "ps", CB),
        (OP, "ps", CP),
    ],
    "ap2": [
        (),
        (OP, "ps", CP)
    ],
    "ps": [
        (),
        ("p", "ps2")
    ],
    "ps2": [
        (),
        (COMMA, "p", "ps2")
    ],

    #
    "bo": [
        ("ba", "bo2")
    ],
    "bo2": [
        (OR2, "ba", "bo2"),
        ()
    ],
    "ba": [
        ("r", "ba2")
    ],
    "ba2": [
        (AND2, "r", "ba2"),
        ()
    ],


    "r": [
        ("e", "r2"),
    ],
    "r2": [
        (),
        (EQ2, "e"),
        (NEQ, "e"),
        (LEQ, "e"),
        (LESS, "e"),
        (GEQ, "e"),
        (GREAT, "e"),

        (EQ2D, "e"),
        (NEQD, "e"),
        (LEQD, "e"),
        (LESSD, "e"),
        (GEQD, "e"),
        (GREATD, "e"),
    ],
    "e": [
        ("t", "e2")
    ],
    "e2": [
        (PLUS, "t", "e2"),
        (MINUS, "t", "e2"),
        (PLUSD, "t", "e2"),
        (MINUSD, "t", "e2"),
        (),
    ],

    "t": [
        ("f", "t2")
    ],
    "t2": [
        (STAR, "t", "e2"),
        (SLASH, "t", "e2"),
        (TIMESD, "t", "e2"),
        (DIVIDED, "t", "e2"),
        (),
    ],

    "f": [
        (MINUS, "f"),
        (MINUSD, "f"),
        ("c", "f2"),
    ],
    "f2": [
        (),
        (COLON2, "f"),
    ],
    "c": [
        ("v", "c2"),
    ],
    "c2": [
        (),
        (OP, "seq", CP, "c2"),
    ],

    "v": [
        (BOOL, ),
        (INT, ),
        (DBL, ),
        (STR, ),
        (ID, ),
        (OB, "seq", CB),
        (OP, "seq", CP),
    ],

}
