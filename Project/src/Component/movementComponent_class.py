from Component.component_class import Component
from Math import Vector2
import pygame
import Paras


class MovementComponent(Component):
    def __init__(self, owner, updateOrder=0):
        super().__init__(owner, updateOrder=0)
        self.mVelocity = Vector2(0, 0)
    
    def ProcessInput(self, keyState):
        super().ProcessInput(keyState)
        
        self.mVelocity.x=0
        self.mVelocity.y=0

        if keyState[pygame.K_LEFT] or keyState[pygame.K_a]:
            self.mVelocity.x = -1
        if keyState[pygame.K_RIGHT] or keyState[pygame.K_d]:
            self.mVelocity.x = 1
        if keyState[pygame.K_UP] or keyState[pygame.K_w]:
            self.mVelocity.y = -1
        if keyState[pygame.K_DOWN] or keyState[pygame.K_s]:
            self.mVelocity.y = 1

        if self.mVelocity.Length() > 0:
            self.mVelocity = self.mVelocity.Normalize().Multiply(Paras.RocketSpeed) 
    
    def Update(self, deltatime):
        super().Update(deltatime)
        
        self.mOwner.mPosition.x += self.mVelocity.x * deltatime
        self.mOwner.mPosition.y += self.mVelocity.y * deltatime
        
        if self.mOwner.mPosition.x<0:
            self.mOwner.mPosition.x=0
        if self.mOwner.mPosition.x>Paras.WINDOWWIDTH:
            self.mOwner.mPosition.x=Paras.WINDOWWIDTH
        if self.mOwner.mPosition.y<0:
            self.mOwner.mPosition.y=0
        if self.mOwner.mPosition.y>Paras.WINDOWHEIGHT:
            self.mOwner.mPosition.y=Paras.WINDOWHEIGHT