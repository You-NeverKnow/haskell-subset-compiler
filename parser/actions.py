from actionFunctions import *

# ---------------------------------------------------- #
# Actions
# ---------------------------------------------------- #
from actionFunctions import Action

actions = {
    "S": [
        Action(2, ignore_eof),
    ],
    "decls": [
        Action(0, make_decls),
        Action(2, add_decl), # :TODO
    ],
    "decl": [
        Action(5, make_decl),
        Action(), # :TODO
    ],
    "E2": [
        Action(3, make_sum),
        Action(3, make_diff),
        Action()
    ],
    "T": [
        Action(),
    ],
    "T2": [
        Action(3, make_prod),
        Action(3, make_div),
        Action()
    ],
    "F": [
        Action(),
        Action(),
        Action(2, make_neg),
        Action(3, make_parenthesis)
    ]
}

