from Math import Vector2, VmiV, VaV, VmN, RandomClamped
import math
import Paras
import random

class BehaviorTypes:
    none = 0x0000
    seek = 0x0002
    pursuit = 0x0004
    wander=0x0008

class SteeringBehaviors:
    def __init__(self, owner):
        self.mOwner = owner
        self.mSteeringForce = Vector2(0,0)
        self.mTarget = owner.mGame.mRocket
        self.mFlag = BehaviorTypes.none
        self.mTargetPos = Vector2(random.uniform(20, Paras.WINDOWWIDTH-20),random.uniform(20, Paras.WINDOWHEIGHT*2/3))
        self.MaxForce = 1000
        theta = random.uniform(0, 2 * math.pi)
        self.m_vWanderTarget = Vector2(Paras.WanderRad * math.cos(theta), 
                                       Paras.WanderRad * math.sin(theta))


    def Seek(self, target_pos):
        desired_velocity = VmiV(target_pos, self.mOwner.mPosition).Normalize().Multiply(Paras.EnemyMaxSpeed)
        return desired_velocity.MinusVec(self.mOwner.mVelocity)

    def Pursuit(self, evader):
        to_evader = VmiV(evader.mPosition, self.mOwner.mPosition)
        self.mOwner.mHeading= VmiV(evader.mPosition, self.mOwner.mPosition).Normalize()
        relative_heading = self.mOwner.mHeading.Dot(Vector2(0,1))

        if to_evader.Dot(self.mOwner.mHeading) > 0 and relative_heading < -0.95:
            return self.Seek(evader.mPosition)

        look_ahead_time = 0
        if evader.mMovementComponent.mVelocity.Length() != 0:
            look_ahead_time = to_evader.Length() / evader.mMovementComponent.mVelocity.Length()

        self.mTargetPos = VaV(VmN(evader.mMovementComponent.mVelocity, look_ahead_time), evader.mPosition)
        return self.Seek(self.mTargetPos)
    
    def Wander(self):
        #TODO
        jitter_this_time_slice = Paras.WanderJitterPerSec * self.mOwner.mTimeElapsed

        self.m_vWanderTarget.x += RandomClamped() * jitter_this_time_slice
        self.m_vWanderTarget.y += RandomClamped() * jitter_this_time_slice
        
        self.m_vWanderTarget = self.m_vWanderTarget.Normalize()

        self.m_vWanderTarget = VmN(self.m_vWanderTarget,Paras.WanderRad)  

        target = VaV(self.m_vWanderTarget, Vector2(Paras.WanderDist, 0))

        target_in_world_space = VaV(target, self.mOwner.mPosition)

        return VmiV(target_in_world_space, self.mOwner.mPosition)

    def on(self, bt):
        return (self.mFlag & bt) == bt

    def SeekOn(self):
        self.mFlag |= BehaviorTypes.seek

    def PursuitOn(self):
        self.mFlag |= BehaviorTypes.pursuit
        
    def WanderOn(self):
        self.mFlag |=BehaviorTypes.wander

    def SeekOff(self):
        if self.on(BehaviorTypes.seek):
            self.mFlag ^= BehaviorTypes.seek

    def PursuitOff(self):
        if self.on(BehaviorTypes.pursuit):
            self.mFlag ^= BehaviorTypes.pursuit

    def WanderOff(self):
        if self.on(BehaviorTypes.wander):
            self.mFlag^=BehaviorTypes.wander

    def AccumulateForce(self, RT, force_to_add):
        magnitude_so_far = RT.Length()
        magnitude_remaining = self.MaxForce - magnitude_so_far
        if magnitude_remaining <= 0.0:
            return False

        magnitude_to_add = force_to_add.Length()

        if magnitude_to_add < magnitude_remaining:
            RT.AddVec(force_to_add)
        else:
            RT.AddVec(force_to_add.Normalize().Multiply(magnitude_remaining))

        return True

    def SumForces(self):
        force = Vector2(0,0)
            
        if self.on(BehaviorTypes.seek):
            force.AddVec(self.Seek(self.mTargetPos))
            if not self.AccumulateForce(self.mSteeringForce, force):
                return self.mSteeringForce

        if self.on(BehaviorTypes.pursuit) and self.mTarget:
            force.AddVec(self.Pursuit(self.mTarget))
            if not self.AccumulateForce(self.mSteeringForce, force):
                return self.mSteeringForce

        if self.on(BehaviorTypes.wander):
            force.AddVec(self.Wander())
            if not self.AccumulateForce(self.mSteeringForce, force):
                return self.mSteeringForce

        return self.mSteeringForce

    def Calculate(self):
        self.mSteeringForce = self.SumForces()
        self.mSteeringForce.Truncate(Paras.EnemyMaxForce)
        return self.mSteeringForce
    
    def Draw(self, surf):
        import pygame
        #pygame.draw.circle(surf, (255,0,0), (int(self.mTargetPos.x), int(self.mTargetPos.y)), 5)