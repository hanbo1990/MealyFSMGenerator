
class StateJumpInfo:
    """
    Defining a class containing all state transition information
    Description: In state have condition, do action, and go to next state
    """

    def __init__(self):
        # starting state
        self.from_state = None
        # end start
        self.to_state = None
        # action to perform when condition occurs in from_state
        self.action = None
        # condition
        self.condition = None
        # transition name
        self.trans_name = None


