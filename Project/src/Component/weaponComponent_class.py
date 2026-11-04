from Component.component_class import Component
from Projectile.laser_class import Laser
from Math import Vector2
import pygame
import Paras
import math
from soundLoader_class import SoundLoader

class WeaponComponent(Component):
    def __init__(self, owner, updateOrder=0):
        super().__init__(owner, updateOrder)
        self.mIsFire=False
        self.mCoolDown=Paras.LaserCoolDownTime
        soundLoader=SoundLoader()
        self.mSound=soundLoader.load_sound('Project\\assets\\Lasers\\Laser_sound.mp3')
    def ProcessInput(self, keyState):
        super().ProcessInput(keyState)
        self.mIsFire=False
        if keyState[pygame.K_SPACE]:
            #Make sure Update always executes in Update
            self.mIsFire=True
        
    def Update(self, deltatime):
        super().Update(deltatime)
        self.mCoolDown-=deltatime
        if self.mCoolDown<0:
            self.mCoolDown=0

        if self.mIsFire and self.mCoolDown==0:
            self._Fire()
            self.mCoolDown=Paras.LaserCoolDownTime
        
    def _Fire(self):
        self.mSound.play()
        Laser(self.mOwner, math.pi/2,'Red',0)