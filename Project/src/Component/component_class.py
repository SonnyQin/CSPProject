
class Component:
    def __init__(self, owner, updateOrder=0):
        self.mOwner=owner
        self.mUpdateOrder=updateOrder
        owner.AddComponent(self)
    
    #virtual
    def ProcessInput(self, keyState):
        pass
    #virtual
    def Update(self, deltatime):
        pass