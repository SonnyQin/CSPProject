from Math import Vector2

class Actor:
    def __init__(self, game, drawOrder):
        self.mGame=game
        self.mPosition=Vector2(0,0)
        self.mHeading=Vector2(0,-1)
        self.mSide=Vector2(1,0)
        self.mRotation=0
        self.mComponents=[]
        self.mDrawOrder=drawOrder
        self.mActive=True
        self.mGame.AddActor(self)
    
    def ProcessInput(self, keyState):
        for cp in self.mComponents:
            cp.ProcessInput(keyState)
        
    def Update(self, deltatime:int):
        for component in self.mComponents:
            component.Update(deltatime)
        
    def Draw(self, surf):
        pass
    def AddComponent(self, c):
        self.mComponents.append(c)
        self.mComponents.sort(key=lambda c: c.mUpdateOrder)
    def RemoveComponent(self, c):
        self.mComponents.remove(c)
        self.mComponents.sort(key=lambda c: c.mUpdateOrder)