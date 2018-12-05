
class StateJumpInfo:

    def __init__(self):
        self.from_state = None
        self.to_state = None
        self.action = None
        self.condition = None


# with from state, condition a ---> action, and next state