from Component.component_class import Component
from imageLoader_class import DrawImage

class AnimationComponent(Component):
    def __init__(self, owner, animArray,updateOrder=0):
        super().__init__(owner, updateOrder)
        self.mAnimArray=animArray
        self.mSelectAnim=animArray['default']
        
    def ProcessInput(self, keyState):
        return super().ProcessInput(keyState)
        
    def Update(self, deltaTime):
        self.mSelectAnim.Update(deltaTime)
    
    def Draw(self, surf):
        DrawImage(surf, self.mSelectAnim.mSelectImage, self.mOwner.mPosition, 0,self.mSelectAnim.mSize)
        