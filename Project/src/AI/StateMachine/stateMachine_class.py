class StateMachine:
    def __init__(self, owner):
        self.pOwner = owner
        self.mCurrentState = None
        self.mPreviousState = None
        self.mGlobalState = None

    def ChangeState(self, new_state):
        self.mPreviousState = self.mCurrentState
        if self.mCurrentState:
            self.mCurrentState.Exit(self.pOwner)
        self.mCurrentState = new_state
        self.mCurrentState.Enter(self.pOwner)

    def ReverToPreviousState(self):
        if self.mPreviousState:
            self.ChangeState(self.mPreviousState)

    def Update(self):
        if self.mGlobalState:
            self.mGlobalState.Execute(self.pOwner)
        if self.mCurrentState:
            self.mCurrentState.Execute(self.pOwner)
