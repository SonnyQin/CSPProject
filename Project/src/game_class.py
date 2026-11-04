import pygame
import Paras
from Actor.rocket_class import Rocket
from AI.Enemies.enemy_class import Enemy
from Actor.Background.background_class import Background
from UI.ui_class import UI
from AI.enemyGenerator_class import EnemyGenerator

class Game:
    def __init__(self):
        self.mActors=[]
        self.mLasers=[]
        self.mEnemies=[]
        self.mIsRunning=True
        self.bContinue=True
        
    def Initialize(self):
        pygame.init()
        self.FPSClock=pygame.time.Clock()
        self.mDisplaySurf=pygame.display.set_mode((Paras.WINDOWWIDTH, Paras.WINDOWHEIGHT))
        pygame.display.set_caption("Rocket")
        
        self.mLevel=1
        self.mUI=UI(self)
        
        self.mBackground=Background(self, 0)
        self.mRocket=Rocket(self, 9999)
        self.mRocket.mPosition.x=Paras.WINDOWWIDTH//2
        self.mRocket.mPosition.y=Paras.RocketStartPosY
        
        # self.mEnemy=Enemy(self, 9999)
        # self.mEnemy.mPosition.x=Paras.WINDOWWIDTH//2
        # self.mEnemy.mPosition.y=100
        
        self.mEnemyGenerator=EnemyGenerator(self)
        self.mEnemyGenerator.Generate()
        
    def Loop(self):
        self.ProcessInput()
        self.Update()
        self.Draw()
        
    def ProcessInput(self):
        if self.mRocket and not self.mRocket.mActive:
            return
        keyState=pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                self.mIsRunning=False
                self.bContinue=False
        
        for actor in self.mActors:
            actor.ProcessInput(keyState)
    
    def Update(self):
        
        if len(self.mEnemies)==0:
            self.mLevel+=1
            self.mEnemyGenerator.Generate()
        
        
        deltatime = self.FPSClock.get_time() / 1000.0
        for actor in self.mActors:
            actor.Update(deltatime)
            
        self.FPSClock.tick(Paras.FPS)
        
    def Draw(self):
        for actor in self.mActors:
            actor.Draw(self.mDisplaySurf)
        self.mUI.Draw(self.mDisplaySurf)
        pygame.display.flip()
    def AddActor(self, actor):
        self.mActors.append(actor)
        self.mActors.sort(key=lambda actor: actor.mDrawOrder)

    def RemoveActor(self, actor):
        try:
            self.mActors.remove(actor)
        except:
            pass
        self.mActors.sort(key=lambda actor: actor.mDrawOrder)
    
        