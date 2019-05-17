from genLexer import make_lexer
from lexer import EOF, PLUS, MINUS, STAR, SLASH, INT, ID, OP, CP,\
    LexerSpecification


# -----------------------------------------------------------------------------|
def is_terminal(symbol) -> bool:
    """

    """

    return type(symbol) == type
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def is_variable(symbol) -> bool:
    """

    """

    return type(symbol) == str

# -----------------------------------------------------------------------------|


class EMPTY: pass


# -----------------------------------------------------------------------------|
def build_table_first(grammar: dict) -> dict:
    """

    """
    table = {var: set() for var in grammar}

    table_changed = True
    
    # Continuously loop till no first set changes
    while table_changed:
        table_changed = False

        for variable in table:
            var_set_len = len(table[variable])

            for rhs in grammar[variable]:
                if not rhs:
                    table[variable].add(EMPTY)
                    continue

                for symbol in rhs:
                    # Terminal
                    if is_terminal(symbol):
                        table[variable].add(symbol)
                        break
                    # Variable
                    else:
                        if EMPTY in table[symbol]:
                            table[variable].update({x for x in table[symbol]
                                                    if x != EMPTY})
                        else:
                            table[variable].update(table[symbol])
                            break

            # Set changed => redo loop
            if var_set_len != len(table[variable]):
                table_changed = True

    return {var: table[var] for var in table}
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def gen_first(grammar: dict):
    """
     Returns a fn that computes
        first(α) = {σ ∈ Σ | α ⇒∗ σβ} ∪ (if α ⇒∗ ε then {ε} else {})

    """

    first_table = build_table_first(grammar)

    def first(rhs: tuple) -> set:
        """
         Implements first(α).
        """
        if not rhs:
            return {EMPTY}
        elif is_terminal(rhs[0]):
            return {rhs[0]}

        return first_table[rhs[0]]

    return first
# -----------------------------------------------------------------------------|  


# -----------------------------------------------------------------------------|
def build_table_follow(grammar: dict, first) -> dict:
    """

    """

    table = {var: set() for var in grammar}

    table_changed = True

    # Continuously loop till no first set changes
    while table_changed:
        table_changed = False
                
        for variable, rules in grammar.items():
            for rhs in rules:
                for i, symbol in enumerate(rhs):
                    # Find variables in rhs side, and update their tables
                    if is_variable(symbol):

                        var_set_len = len(table[symbol])

                        # Get first() of succeeding set of symbols
                        follow_set = first(rhs[i+1:])
                        table[symbol].update({x for x in follow_set
                                              if x != EMPTY})

                        # ε in follow => add follow of V to follow(A)
                        if EMPTY in follow_set:

                            table[symbol].update(table[variable])

                        # Set changed => redo loop
                        if var_set_len != len(table[symbol]):
                            table_changed = True

    return table
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|    
def gen_follow(grammar: dict, first):
    """
        Generates a fn that computes:
        FOLLOW(A) = {σ ∈ Σ | S ⇒+ αAσβ} ∪ (if S ⇒+ αA then {ε} else {})
    """

    follow_table = build_table_follow(grammar, first)

    def follow(variable: str) -> set:
        """
         Implements follow(A).
        """
        return follow_table[variable]

    return follow

# -----------------------------------------------------------------------------|  


# -----------------------------------------------------------------------------|    
def gen_predict(grammar: dict):
    """
     
    """

    first = gen_first(grammar)
    follow = gen_follow(grammar, first)

    def predict(rule: tuple) -> set:
        # debug
        # print(f"rule[1] = {rule[1]}")

        _first = first(rule[1])
        _follow = follow(rule[0]) if EMPTY in _first else set()

        return _first.union(_follow)

    return predict
# -----------------------------------------------------------------------------|


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


# -----------------------------------------------------------------------------|
def get_augmented_grammar(grammar, action_dict) -> dict:
    """

    """
    grammar_actions = {var: [] for var in grammar}

    # Augment grammar with actions
    for var in grammar:
        for i, _ in enumerate(grammar[var]):
            grammar_actions[var].append(grammar[var][i]+(action_dict[var][i],))

    return grammar_actions
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def gen_oracle(grammar: dict, action_dict: dict):
    """

    """

    predict = gen_predict(grammar)

    grammar_actions = get_augmented_grammar(grammar, action_dict)

    # For each rule, fill the oracle table
    table = {var: {} for var in grammar}
    for var in grammar:
        for i, rhs in enumerate(grammar[var]):
            predictions = predict((var, rhs))

            for prediction in predictions:
                if prediction in table[var]:
                    raise SyntaxError("Language is not LL1")
                else:
                    table[var][prediction] = grammar_actions[var][i]
    
    #debug
    # print("Oracle: ")
    # for x in table:
    #     for y in table[x]:
    #         print(f"{x}, {y}")
    #         print(f"table = {table[x][y]}")

    def oracle(variable: str, terminal: type) -> tuple:
        return table[variable][terminal]

    return oracle
# -----------------------------------------------------------------------------|


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


class SumInt(Operator): pass
class DifferenceInt(Operator): pass
class ProductInt(Operator): pass
class QuotientInt(Operator): pass


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

        return f"(-{self.x})"
    # -------------------------------------------------------------------------|
# =============================================================================|


# -----------------------------------------------------------------------------|    
def make_parser(grammar: dict, action_dict: dict):
    """

    """

    oracle = gen_oracle(grammar, action_dict)
    aug_grammar = get_augmented_grammar(grammar, action_dict)

    parse_stack = [*aug_grammar["S"][0][::-1]]
    sem_stack = []

    def parser(tokens: list):

        i = 0
        nonlocal sem_stack, parse_stack

        while parse_stack:
            stack_top = parse_stack.pop()

            if is_terminal(stack_top):
                # If terminal, put in semantic stack
                sem_stack.append(tokens[i].evaluate())
                i += 1
            elif is_variable(stack_top):
                # If variable, find rule that corresponds to that var and token
                rule = oracle(variable = stack_top, terminal = type(tokens[i]))
                parse_stack += rule[::-1]
            else:
                # One rule processed => combine tokens from
                # semantic stack into logical units
                n, f = stack_top.args_len, stack_top.action
                if f:
                    args = sem_stack[-n:]
                    sem_stack = sem_stack[:-n]
                    value = f(*args)
                    sem_stack.append(value)

        return sem_stack[0]

    return parser
# -----------------------------------------------------------------------------|  


# -----------------------------------------------------------------------------|
def main():
    """

    """

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
    # ----------------------------- #

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

    string = "4+(-5)"
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)
    parser = make_parser(grammar, actions)
    print(parser(tokens))
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()
