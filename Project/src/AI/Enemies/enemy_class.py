from Actor.actor_class import Actor
from Component.animationComponent_class import AnimationComponent
from Component.animation_class import Animation, ExplosionAnim
from Component.collisionComponent_class import CollisionComponent
from AI.StateMachine.stateMachine_class import StateMachine
from AI.StateMachine.States.enemyStates import EnemyGlobalState,EnemyWanderState
from AI.SteeringBehavior.steeringBehavior_class import SteeringBehaviors
from Math import CircleCollider, Vector2, VdN, VmN
from Projectile.laser_class import Laser
import Paras
import math
import random
from soundLoader_class import SoundLoader

class Enemy(Actor):
    def __init__(self, game,drawOrder):
        super().__init__(game, drawOrder)
        self.mHeading=Vector2(0,1)
        self.mSide=Vector2(-1,0)
        self.mLaserColor=random.choice(['Red', 'Green', 'Blue', 'Purple'])
        game.mEnemies.append(self)
        self.mAnimationComponent=AnimationComponent(self, {'default':Animation(['Project\\assets\\UFO\\UFO01.png','Project\\assets\\UFO\\UFO02.png','Project\\assets\\UFO\\UFO03.png','Project\\assets\\UFO\\UFO04.png','Project\\assets\\UFO\\UFO05.png','Project\\assets\\UFO\\UFO06.png'],0.6,True),'explosion':ExplosionAnim()},0)
        self.mCollisionComponent=CollisionComponent(self, CircleCollider(Vector2(0,0),17),0)
        self.mTimer=0
        self.mTargetTimer=random.uniform(0, 5)
        self.mSteeringBehaviors=SteeringBehaviors(self)
        self.type='Enemy'
        self.mVelocity=Vector2(0,0)
        
        self.mStateMachine=StateMachine(self)
        self.mStateMachine.mGlobalState=EnemyGlobalState.get_instance()
        self.mStateMachine.ChangeState(EnemyWanderState.get_instance())
        
        self.mCoolDown=random.uniform(0,Paras.EnemyLaserCoolDownTime)
        soundLoader=SoundLoader()
        self.mLaserSound=soundLoader.load_sound('Project\\assets\\Lasers\\Laser_sound.mp3')
        self.mExplosionSound=soundLoader.load_sound('Project\\assets\\explosion\\Explosion_sound.mp3')
        
    def Update(self, deltatime: int):
        super().Update(deltatime)
        self.mTimeElapsed=deltatime
        if self.mActive==False:
            self.mTimer+=deltatime
        if self.mTimer>=0.7:
            self.mGame.RemoveActor(self)
            self.mGame.mEnemies.remove(self)
        self.mStateMachine.Update()
        
        self.mTargetTimer+=deltatime
        if self.mTargetTimer>=5:
            self._ResetTarget()
            self.mTargetTimer=0
        
        SteeringForce=self.mSteeringBehaviors.Calculate().Copy();

        Acceleration= VdN(SteeringForce,Paras.EnemyMass);
        
        Velocity=Vector2(self.mVelocity.x, self.mVelocity.y)
        Velocity.AddVec(VmN(Acceleration,deltatime));
        Velocity.Truncate(Paras.EnemyMaxSpeed);
        
        self.mVelocity.x=Velocity.x
        self.mVelocity.y=Velocity.y
        
        #Update movement
        self.mPosition.x+=Velocity.x*deltatime
        self.mPosition.y+=Velocity.y*deltatime
        
        if self.mPosition.x<0:
            self.mPosition.x=0
        if self.mPosition.x>Paras.WINDOWWIDTH:
            self.mPosition.x=Paras.WINDOWWIDTH
        if self.mPosition.y<0:
            self.mPosition.y=0
        if self.mPosition.y>Paras.WINDOWHEIGHT*2/3:
            self.mPosition.y=Paras.WINDOWHEIGHT*2/3
        
        #Always fire at player
        self.mCoolDown-=deltatime
        if self.mCoolDown<0:
            self.mCoolDown=0

        if self.mCoolDown==0:
            self._Fire()
            self.mCoolDown=Paras.EnemyLaserCoolDownTime
        
    def _Fire(self):
        if not self.mGame.mRocket:
            return
        target = self.mGame.mRocket.mPosition
        targetAngle = math.atan2(target.y - self.mPosition.y, target.x - self.mPosition.x)
        angleOffset = random.uniform(-Paras.EnemyFireOffset, Paras.EnemyFireOffset)
        fireAngle = targetAngle + angleOffset
        fireAngle+=math.pi
        self.mLaserSound.play()
        Laser(self, fireAngle, self.mLaserColor, 0)
    
    def _ResetTarget(self):
        self.mSteeringBehaviors.mTargetPos.x=random.uniform(20, Paras.WINDOWWIDTH-20)
        self.mSteeringBehaviors.mTargetPos.y=random.uniform(20, Paras.WINDOWHEIGHT*2/3)
        
    def Draw(self, surf):
        super().Draw(surf)
        self.mAnimationComponent.Draw(surf)
        self.mCollisionComponent.Draw(surf)
        self.mSteeringBehaviors.Draw(surf)
    
    def onCollide(self, instigator):
        self.mExplosionSound.play()
        self.mAnimationComponent.mSelectAnim=self.mAnimationComponent.mAnimArray['explosion']
        self.mActive=False