import random
from AI.Enemies.enemy_class import Enemy
import Paras

class EnemyGenerator:
    def __init__(self, game):
        self.mGame=game
    def Generate(self):
        num=self.mGame.mLevel
        for i in range(num):
            enemy=Enemy(self.mGame,9999)
            enemy.mPosition.x=random.uniform(20, Paras.WINDOWWIDTH-20)
            enemy.mPosition.y=random.uniform(20, Paras.WINDOWHEIGHT*2/3)