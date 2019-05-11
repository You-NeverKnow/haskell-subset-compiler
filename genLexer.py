from collections import defaultdict
from regex_primitives import *


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
            "whitespace":Range(Char(chr(0)), Char(chr(32))),
            "upper":Range(Char("A"), Char("Z")),
            "lower":Range(Char("a"), Char("z")),
            "letter":Or(Name("lower"), Name("upper")),
            "letters":Plus(Name("letter")),
            "digit":Range(Char("0"), Char("9")),
            "digits":Plus(Name("digit"))
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

    for name, regex in binding_list.items():
        binding_list[name] = regular_from_extended(
                                extended_from_named(regex, binding_list))
    return binding_list
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
        regex = regular_from_extended(extended_regex.r)
        return Star(regex)

    elif type(extended_regex) == str:
        if len(extended_regex) == 1:
            return Char(extended_regex)
        regex = regular_from_extended(extended_regex[1:])
        return Sequence(Char(extended_regex[0]), regex)

    elif type(extended_regex) == Optional:
        regex = regular_from_extended(extended_regex.r)
        return Or(ε(), regex)

    elif type(extended_regex) == Plus:
        regex = regular_from_extended(extended_regex.r)
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
                                             ord(extended_regex.end.ch)+1)]
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
    def __init__(self, transition: dict, start: int, final: int):
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
        return NFA(transition, start, final)

    elif type(regex) == Char:
        transition[(start, regex.ch)].add(final)
        return NFA(transition, start, final)

    elif type(regex) == Or:
        nfa_r1 = nfa_from_regex(regex.r1)
        nfa_r2 = nfa_from_regex(regex.r2)

        transition[(start, ε)].add(nfa_r1.start)
        transition[(start, ε)].add(nfa_r2.start)
        transition[(nfa_r1.final, ε)].add(final)
        transition[(nfa_r2.final, ε)].add(final)

        transition = defaultdict(set, {**transition, **nfa_r1.transition,
                                       **nfa_r2.transition})
        return NFA(transition, start, final)

    elif type(regex) == Sequence:
        nfa_r1 = nfa_from_regex(regex.r1)
        nfa_r2 = nfa_from_regex(regex.r2)

        transition[(start, ε)].add(nfa_r1.start)
        transition[(nfa_r1.final, ε)].add(nfa_r2.start)
        transition[(nfa_r2.final, ε)].add(final)

        transition = defaultdict(set, {**transition, **nfa_r1.transition,
                                       **nfa_r2.transition})
        return NFA(transition, start, final)

    elif type(regex) == Star:
        # Case 0 times repeat
        transition[(start, ε)].add(final)

        # Case more than one repeat
        nfa_r = nfa_from_regex(regex.r)
        transition[(start, ε)].add(nfa_r.start)
        transition[(nfa_r.final, ε)].add(final)
        transition[(nfa_r.final, ε)].add(nfa_r.start)

        transition = defaultdict(set, {**transition, **nfa_r.transition})
        return NFA(transition, start, final)
    else:
        # debug
        print(f"regex ={regex}")
        
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
    final = gen_state()
        
    transition = defaultdict(set)

    for nfa in nfas:
        transition[(start, ε)].add(nfa.start)
        transition[(nfa.final, ε)].add(final)
        transition = defaultdict(set, {**transition, **nfa.transition})

    return NFA(transition, start, final)
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def _get_ε_closure(visited: set, transition: defaultdict,
                   ε_closure: defaultdict, state: int) -> None:
    """

    """

    if state in visited:
        return

    visited.add(state)
    ε_closure[state] = set()

    if (state, ε) in transition:
        for ε_transition_state in transition[(state, ε)]:
            _get_ε_closure(visited, transition, ε_closure, ε_transition_state)
            ε_closure[state].union(ε_closure[ε_transition_state])
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def get_ε_closure(transition: defaultdict) -> dict:
    """

    """

    ε_closure, visited = {}, set()
    for state in range(state_counter):
        _get_ε_closure(visited, transition, ε_closure, state)
        
    
    # debug
    print(f"ε_closure[788] = {ε_closure[788]}")
    
    return ε_closure
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def apply_nfa(ε_closure: dict, transition: dict, final_states: set, string: str,
              index: int, starting_states: set,
              reached_final_states: set) -> set:
    """

    """
    
    # debug
    print(f"starting_states = {starting_states}")
    
    if len(starting_states) == 0:
        return reached_final_states

    if index == len(string):
        raise SyntaxError("Syntax error in code file")

    next_states = set()
    for state in starting_states:
        _next_states = apply_trans(transition, state, string[index])
        for next_state in _next_states:
            if next_state in final_states:
                reached_final_states.add((next_state, index))
            next_states.union(ε_closure[next_state])

    return apply_nfa(ε_closure, transition, final_states, string,
                     index + 1, next_states, reached_final_states)
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def identify_lexeme(nfa: NFA, ε_closure: dict,
                    string: str, final_states: set,
                    index: int) -> tuple:
    """

    """

    if index == len(string):
        return None, index
    transition, start, _ = nfa.transition, nfa.start, nfa.final
    # debug
    print(f"string ={string}")
    # debug
    print(f"index = {index}")

    reached_final_states = apply_nfa(ε_closure, transition, final_states,
                                     string, index, ε_closure[start], set())

    return max(reached_final_states, key= lambda x: (x[1], -x[0]))
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def make_lexer(spec: LexerSpecification):
    """

    """

    gen_actions = dict()
    environment = build_env(spec.binding_list)

    nfas = set()
    for named_regex, action in spec.patterns:
        extended_regex = extended_from_named(named_regex, environment)
        regex = regular_from_extended(extended_regex)
        nfa = nfa_from_regex(regex)
        nfas.add(nfa)

        # Create action binding list
        assert nfa.final not in gen_actions
        gen_actions[nfa.final] = action

    spec_nfa = glue_nfas(nfas)
    final_states = {nfa.final for nfa in nfas}
    ε_closure = get_ε_closure(spec_nfa.transition)

    def _lexer(string: str):
        tokens = []
        lexeme_start = 0
        while lexeme_start < len(string):
            final_state, lexeme_end = identify_lexeme(spec_nfa, ε_closure,
                                                      string, final_states,
                                                      lexeme_start)
            state_action = gen_actions[final_state]
            if action:
                token = state_action(string[lexeme_start: lexeme_end])
                tokens.append(token)
        return tokens

    return _lexer
# -----------------------------------------------------------------------------|


# -----------------------------------------------------------------------------|
def main():
    """

    """

    # string = sys.argv[1]
    string = "2+3*4"
    _lexer = make_lexer(LexerSpecification())
    tokens = _lexer(string)
    print(tokens)


# -----------------------------------------------------------------------------|


if __name__ == '__main__':
    main()

