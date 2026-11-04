from Actor.actor_class import Actor
from Component.movementComponent_class import MovementComponent
from Component.animationComponent_class import AnimationComponent
from Component.weaponComponent_class import WeaponComponent
from Component.collisionComponent_class import CollisionComponent
from Component.animation_class import Animation, ExplosionAnim
from Math import Collider,Vector2
import Paras
from soundLoader_class import SoundLoader
class Rocket(Actor):
    def __init__(self, game, drawOrder):
        super().__init__(game, drawOrder)
        self.mHeading=Vector2(0,-1)
        self.mSide=Vector2(1,0)
        self.mHealth=Paras.RocketHealth
        self.mMovementComponent=MovementComponent(self)
        self.mAnimationComponent=AnimationComponent(self, {'default':Animation(['Project\\assets\\Ship\\Ship01.png','Project\\assets\\Ship\\Ship02.png','Project\\assets\\Ship\\Ship03.png','Project\\assets\\Ship\\Ship04.png' ],1, True),'explosion':ExplosionAnim()},0)
        self.mWeaponComponent=WeaponComponent(self)
        self.mCollisionComponent=CollisionComponent(self, Collider(Vector2(self.mPosition.x,self.mPosition.y), 17, 50),0)
        self.mTimer=0
        self.type='Rocket'
        soundLoader=SoundLoader()
        self.mExplosionSound=soundLoader.load_sound('Project\\assets\\explosion\\Explosion_sound.mp3')
    def ProcessInput(self, keyState):
        super().ProcessInput(keyState)
        
    def Update(self, deltatime: int):
        super().Update(deltatime)
        if self.mActive==False:
            self.mTimer+=deltatime
        if self.mTimer>=0.7:
            self.mGame.RemoveActor(self)
            self.mGame.mRocket=None
            self.mGame.mIsRunning=False
        
        
    def Draw(self, surf):
        super().Draw(surf)
        self.mAnimationComponent.Draw(surf)
        self.mCollisionComponent.Draw(surf)
        
    def onCollide(self, instigator):
        self.mAnimationComponent.mSelectAnim=self.mAnimationComponent.mAnimArray['explosion']
        self.mActive=False
        self.mExplosionSound.play()