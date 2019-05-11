from collections import defaultdict

from lexer import LexerSpecification
from regex_primitives import *


# -----------------------------------------------------------------------------|    
def extended_from_named(named_regex, binding_list: dict):
    """
     
    """

    if type(named_regex) == Name:
        return binding_list[named_regex.name]

    elif type(named_regex) == Or:
        return Or(extended_from_named(named_regex.r1, binding_list),
                  extended_from_named(named_regex.r2, binding_list))

    elif type(named_regex) == Sequence:
        return Sequence(extended_from_named(named_regex.r1, binding_list),
                        extended_from_named(named_regex.r2, binding_list))

    elif type(named_regex) == Star:
        return Star(extended_from_named(named_regex.r, binding_list))

    elif type(named_regex) == Optional:
        return Optional(extended_from_named(named_regex.r, binding_list))

    elif type(named_regex) == Plus:
        return Plus(extended_from_named(named_regex.r, binding_list))

    else:
        return named_regex
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|    
def build_env(binding_list):
    """

    """

    environment = dict()
    for name, regex in binding_list.items():
        environment[name] = regular_from_extended(
                                extended_from_named(regex, binding_list))
    return environment
# -----------------------------------------------------------------------------|  


# -----------------------------------------------------------------------------|
def create_Or_Tree(options) -> Or:
    """

    """

    if len(options) == 2:
        return Or(*options)
    else:
        return Or(options[0], create_Or_Tree(options[1:]))
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|    
def regular_from_extended(extended_regex):
    """

    """

    if type(extended_regex) == Or:
        r1 = regular_from_extended(extended_regex.r1)
        r2 = regular_from_extended(extended_regex.r2)
        return Or(r1, r2)

    elif type(extended_regex) == Sequence:
        r1 = regular_from_extended(extended_regex.r1)
        r2 = regular_from_extended(extended_regex.r2)
        return Sequence(r1, r2)

    elif type(extended_regex) == Star:
        regex = regular_from_extended(extended_regex)
        return Star(regex)

    elif type(extended_regex) == str:
        if len(extended_regex) == 1:
            return Char(extended_regex)
        regex = regular_from_extended(extended_regex[1:])
        return Sequence(Char(extended_regex[0]), regex)

    elif type(extended_regex) == Optional:
        regex = regular_from_extended(extended_regex)
        return Or(ε(), regex)

    elif type(extended_regex) == Plus:
        regex = regular_from_extended(extended_regex)
        return Or(regex, Star(regex))

    elif type(extended_regex) == Σ:
        Σ_str = [chr(i) for i in range(127)]
        return create_Or_Tree(Σ_str)

    elif type(extended_regex) == Σ_except:
        Σ_except_str = [chr(i) for i in range(127)
                        if chr(i) not in extended_regex.except_set]
        return create_Or_Tree(Σ_except_str)

    elif type(extended_regex) == Range:
        range_chars = [chr(i) for i in range(ord(extended_regex.start.ch),
                                             ord(extended_regex.end.ch+1))]
        return create_Or_Tree(range_chars)
    else:
        # ε, Char
        return extended_regex

# -----------------------------------------------------------------------------|


# =============================================================================|
class NFA:
    """

    """
    # -------------------------------------------------------------------------|
    def __init__(self, transition: dict, start: int, final: set):
        """
        Constructor for NFA
        """
        self.transition = transition
        self.start = start
        self.final = final
    # -------------------------------------------------------------------------|

# =============================================================================|


state_counter = 0


# -----------------------------------------------------------------------------|
def gen_state():
    """

    """
    global state_counter
    new_state = state_counter
    state_counter += 1
    return new_state
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|    
def nfa_from_regex(regex) -> NFA:
    """

    """
    start = gen_state()
    final = gen_state()
    transition = defaultdict(set)

    if type(regex) == ε:
        transition[(start, ε)].add(final)
        return NFA(transition, start, {final})

    elif type(regex) == Char:
        transition[(start, regex.ch)].add(final)
        return NFA(transition, start, {final})

    elif type(regex) == Or:
        nfa_r1 = nfa_from_regex(regex.r1)
        nfa_r2 = nfa_from_regex(regex.r2)

        transition[(start, ε)].add(nfa_r1.start)
        transition[(start, ε)].add(nfa_r2.start)

        nfa_r1.transition[(nfa_r1.final, ε)].add(final)
        nfa_r2.transition[(nfa_r2.final, ε)].add(final)

        transition = {**transition, **nfa_r1.transition, **nfa_r2.transition}
        return NFA(transition, start, {final})

    elif type(regex) == Sequence:
        nfa_r1 = nfa_from_regex(regex.r1)
        nfa_r2 = nfa_from_regex(regex.r2)

        transition[(start, ε)].add(nfa_r1.start)
        nfa_r1.transition[(nfa_r1.final, ε)].add(nfa_r2.start)
        nfa_r2.transition[(nfa_r2.final, ε)].add(final)

        transition = {**transition, **nfa_r1.transition, **nfa_r2.transition}
        return NFA(transition, start, {final})

    elif type(regex) == Star:
        # Case 0 times repeat
        transition[(start, ε)].add(final)

        # Case more than one repeat
        nfa_r = nfa_from_regex(regex.r)
        transition[(start, ε)].add(nfa_r.start)

        nfa_r.transition[(nfa_r.final, ε)].add(final)
        nfa_r.transition[(nfa_r.final, ε)].add(nfa_r.start)

        transition = {**transition, **nfa_r.transition}
        return NFA(transition, start, {final})
    else:
        raise Exception("Not a regex")
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def apply_trans(transition: dict, state: int, ch) -> set:
    """

    """

    if type(ch) == ε:
        return transition[(state, ε)]
    else:
        return transition[(state, ch)]
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|    
def glue_nfas(nfas: iter) -> NFA:
    """

    """
    start = gen_state()
    transition = defaultdict(set)
    final = set()

    for nfa in nfas:
        transition[(start, ε)].add(nfa.start)
        transition = {**transition, **nfa.transition}
        final.union(nfa.final)

    return NFA(transition, start, final)
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def get_ε_closure(transition) -> dict:
    """

    """

    ε_closure = defaultdict(set)

    return ε_closure
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def identify_lexeme(nfa: NFA, ε_closure: dict,
                    string: str, index: int) -> tuple:
    """

    """

    if index == len(string):
        return None, None, index
    transition, start, final = nfa.transition, nfa.start, nfa.final
    starting_states = ε_closure[start]
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def make_lexer(spec: LexerSpecification):
    """

    """

    gen_actions = dict()
    environment = build_env(spec.binding_list)

    nfas = set()
    for regex, action in spec.patterns:
        nfa = nfa_from_regex(regular_from_extended(
                                    extended_from_named(regex, environment)))
        nfas.add(nfa)

        # Create action binding list
        for final in nfa.final:
            assert final not in gen_actions
            gen_actions[final] = action

    spec_nfa = glue_nfas(nfas)
    ε_closure = get_ε_closure(spec_nfa.transition)

    def _lexer(string: str):
        tokens = []
        i = 0
        while i < len(string):
            final_state, lexeme, i = identify_lexeme(spec_nfa, ε_closure,
                                                     string, i)
            state_action = gen_actions[final_state]
            if action:
                token = state_action(lexeme)
                tokens.append(token)
        return tokens

    return _lexer
# -----------------------------------------------------------------------------|
