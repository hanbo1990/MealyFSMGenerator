
def sm_state_common(sm_name):
    return sm_name.upper() + "_STATE__"


def sm_condition_common(sm_name):
    return sm_name.upper() + "_CONDITION__"


def state_enum_type(sm_name):
    return sm_name + "State_e"


def state_type(sm_name):
    return sm_name + "State_t"


def condition_enum_type(sm_name):
    return sm_name + "Condition_e"


def transition_name(sm_name):
    return sm_name + "Transition_t"


def transition_table_name(sm_name):
    return sm_name + "TransitionTable"


def init_func_name(sm_name):
    return sm_name + "_Init"


def tick_func_name(sm_name):
    return sm_name + "_Tick"


def header_guard(sm_name):
    return sm_name.upper() + "_H"

