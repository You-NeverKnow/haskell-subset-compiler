from lexer import EOF, PLUS, MINUS, STAR, SLASH, INT, ID, OP, CP


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


class Empty: pass


# -----------------------------------------------------------------------------|
def without_empty(_set: set) -> set:
    """

    """

    if len(_set) == 1 and _set.pop() == Empty:
        return {Empty}

    return {x for x in _set if x != Empty}
# -----------------------------------------------------------------------------|


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

            # For each rule for the variable, update its set
            for rhs in grammar[variable]:
                # ε
                if not rhs:
                    table[variable].add(Empty)
                # Terminal
                elif is_terminal(rhs[0]):
                    table[variable].add(rhs[0])
                # Variable
                else:
                    table[variable].update(table[rhs[0]])

            # Set changed => redo loop
            if var_set_len != len(table[variable]):
                table_changed = True

    return {var: without_empty(table[var]) for var in table}
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
            return {Empty}
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
            for var, rhs in rules:
                for i, symbol in enumerate(rhs):
                    # Find variables in rhs side, and update their tables
                    if is_variable(symbol):
                        var_set_len = len(table[symbol])

                        follow_set = first(rhs[i+1:])
                        # debug
                        print(f"follow_set = {follow_set}")

                        table[symbol].update(without_empty(follow_set))

                        if Empty in follow_set:
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
def main():
    """

    """

    grammar = {
        "S": {
            ("E", EOF),
        },
        "E": {
            ("T", "E2"),
        },
        "E2": {
            (PLUS, EOF),
            (MINUS, EOF),
            (),
        },
        "T": {
            ("F", "T2")
        },
        "T2": {
            (STAR, "F", "T2"),
            (SLASH, "F", "T2"),
            ()
        },
        "F": {
            (INT,),
            (ID,),
            (MINUS, "F"),
            (OP, "E", CP),
        }
    }

    first = gen_first(grammar)

    # for var, rules in grammar.items():
    #     for rhs in rules:
    #         print(var, ":", first(rhs))

    follow = gen_follow(grammar, first)

    for var in grammar:
        print(var, ":", follow(var))
# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()
