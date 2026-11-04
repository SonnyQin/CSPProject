from Actor.actor_class import Actor
from Component.collisionComponent_class import CollisionComponent
from Math import Collider, Vector2
from imageLoader_class import ImageLoader, DrawImage
import math
import Paras

class Laser(Actor):
    def __init__(self, instigator, rotation, color,drawOrder):
        super().__init__(instigator.mGame, drawOrder)
        instigator.mGame.mLasers.append(self)
        self.mPosition.x=instigator.mPosition.x
        self.mPosition.y=instigator.mPosition.y
        self.mInstigator=instigator
        self.mRotation=rotation
        self.mCollisionComponent=CollisionComponent(self, Collider(Vector2(0,0), 37, 3, rotation),0)
        self.type='Laser'
        
        imgloader=ImageLoader()
        if color=='Red':
            self.mSelectImage=imgloader.load_image('Project\\assets\\Lasers\\Laser_red.png')
        elif color=='Blue':
            self.mSelectImage=imgloader.load_image('Project\\assets\\Lasers\\Laser_blue.png')
        elif color=='Green':
            self.mSelectImage=imgloader.load_image('Project\\assets\\Lasers\\Laser_green.png')
        elif color=='Purple':
            self.mSelectImage=imgloader.load_image('Project\\assets\\Lasers\\Laser_purple.png')
    
    def Update(self, deltatime):
        super().Update(deltatime)
        self.mPosition.x+=deltatime*math.cos(self.mRotation)*Paras.LaserVelocity
        self.mPosition.y+=deltatime*math.sin(self.mRotation)*Paras.LaserVelocity
        
        if self.mPosition.y<-30 or self.mPosition.y>Paras.WINDOWHEIGHT+30:
            self.mGame.RemoveActor(self)
            self.mGame.mLasers.remove(self)
    
    def Draw(self, surf):
        DrawImage(surf, self.mSelectImage, self.mPosition, math.pi*2- self.mRotation,1.0)
        self.mCollisionComponent.Draw(surf)