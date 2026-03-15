from .state import State


__state = None



def set_state(state: State):
    global __state
    __state = state


def get_state() -> State | None:
    return __state
