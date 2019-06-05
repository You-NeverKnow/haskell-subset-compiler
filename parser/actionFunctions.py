# =============================================================================|
class Action:
    """

    """

    # -------------------------------------------------------------------------|
    def __init__(self, args_len = 0, action = None):
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


# =============================================================================|
class Operator:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self, x, y):
        """
        Constructor for Plus
        """
        self.x = x
        self.y = y

        if type(self) == SumInt:
            self.sign = "+"
        elif type(self) == DifferenceInt:
            self.sign = "-"
        elif type(self) == ProductInt:
            self.sign = "*"
        elif type(self) == QuotientInt:
            self.sign = "/"

    # -------------------------------------------------------------------------|
    # -------------------------------------------------------------------------|
    def __repr__(self, ):
        """

        """

        return f"({self.sign} {self.x} {self.y})"
    # -------------------------------------------------------------------------|
# =============================================================================|


# =============================================================================|
class Negative:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self, x):
        """
        Constructor for Negative
        """
        self.x = x
    # -------------------------------------------------------------------------|

    # -------------------------------------------------------------------------|
    def __repr__(self, ):
        """

        """

        return f"(-n{self.x})"
    # -------------------------------------------------------------------------|
# =============================================================================|


# ----------------------------- #
# Parsed data structures
# ----------------------------- #
class SumInt(Operator): pass
class DifferenceInt(Operator): pass
class ProductInt(Operator): pass
class QuotientInt(Operator): pass


# =============================================================================|
class Declarations:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self):
        """
        Constructor for Declarations
        """
        self.decls = []
    # -------------------------------------------------------------------------|

    # -------------------------------------------------------------------------|

    def __repr__(self):
        """

        """
        return f"(decls\n\t{self.decls})"
    # -------------------------------------------------------------------------|
# =============================================================================|


# =============================================================================|
class DataDecl:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self, identifier, formals, constructors):
        """
        Constructor for Declarations
        """
        self.identifier = identifier
        self.formals = formals
        self.constructors = constructors
    # -------------------------------------------------------------------------|

    # -------------------------------------------------------------------------|

    def __repr__(self):
        """

        """
        return f"(Decl({self.formals}, {self.constructors})"
    # -------------------------------------------------------------------------|
# =============================================================================|

# =============================================================================|
class TypeDecl:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self, identifier, dtype):
        """
        Constructor for TypeDecl
        """
        self.identifier = identifier
        self.dtype = dtype
    # -------------------------------------------------------------------------|
# =============================================================================|


# =============================================================================|
class Assignment:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self, identifier, value):
        """
        Constructor for Assi
        """
        self.identifier = identifier
        self.value = value
    # -------------------------------------------------------------------------|
# =============================================================================|

# ----------------------------- #
# Action-functions
# ----------------------------- #
def ignore_eof(decls, eof): return decls


def make_decls(): return Declarations()


def make_data_decl(data_token, id_token, formals, eq_sign, constructors):
    return DataDecl(id_token, formals, constructors)


def make_type_decl(identifier, colon, dtype): return TypeDecl(identifier, dtype)


def make_assignment(identifier, eq, value):
    return Assignment(identifier, value)


def add_decl(decl, decls):
    decls.decls.append(decl)
    return decls


def make_sum(x, sign, y): return SumInt(x, y)


def make_diff(x, sign, y): return DifferenceInt(x, y)


def make_prod(x, sign, y): return ProductInt(x, y)


def make_div(x, sign, y): return QuotientInt(x, y)


def make_neg(sign, x): return Negative(x)


def make_parenthesis(op, x, cp): return x


