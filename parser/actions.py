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
        Action(5, make_data_decl),
        Action(),
    ],
    "decls2": [
        Action(3, make_type_decl),
        Action(3, make_assignment),
        Action()
    ],
    "decls3": [
        Action(6, make_function),
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

