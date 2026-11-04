from Component.component_class import Component

class CollisionComponent(Component):
    def __init__(self, owner, collider,updateOrder):
        super().__init__(owner, updateOrder)
        self.mCollider=collider

    def Update(self, deltaTime):
        self.mCollider.mPosition.x=self.mOwner.mPosition.x
        self.mCollider.mPosition.y=self.mOwner.mPosition.y
        
        game=self.mOwner.mGame
        
        #Only use Laser to test other entities
        if self.mOwner.type=='Laser':
            #No frinedly fire
            if self.mOwner.mInstigator.type=='Enemy':
                if game.mRocket and self.mCollider.IntersectCollider(game.mRocket.mCollisionComponent.mCollider):
                    #print('Rocket Down')
                    game.mRocket.onCollide(self.mOwner)
                    game.RemoveActor(self.mOwner)
            elif self.mOwner.mInstigator.type=='Rocket':
                for enemy in game.mEnemies:
                    if self.mCollider.IntersectCircleCollider(enemy.mCollisionComponent.mCollider):
                        #print('Enemy Down')
                        enemy.onCollide(self.mOwner)
                        game.RemoveActor(self.mOwner)

    def Draw(self, surf):
        self.mCollider.Draw(surf)