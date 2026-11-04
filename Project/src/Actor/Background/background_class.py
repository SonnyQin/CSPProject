from Actor.actor_class import Actor
from imageLoader_class import ImageLoader

import pygame
import Paras

from Actor.Background.backgroundLayer_class import BackgroundLayer


class Background(Actor):
    def __init__(self, game, drawOrder):
        super().__init__(game, drawOrder)
        imgloader=ImageLoader()
        self.mLayerArray=[]
        self.mLayerArray.append(BackgroundLayer(imgloader.load_image('Project\\assets\\Background\\Farback01.png'),0))
        self.mLayerArray.append(BackgroundLayer(imgloader.load_image('Project\\assets\\Background\\Farback02.png'), -Paras.WINDOWHEIGHT))
        self.mLayerArray.append(BackgroundLayer(imgloader.load_image('Project\\assets\\Background\\Stars.png'),0))
        self.mLayerArray.append(BackgroundLayer(imgloader.load_image('Project\\assets\\Background\\Stars.png'), -Paras.WINDOWHEIGHT))
        self.mStars=imgloader.load_image('Project\\assets\\Background\\Stars.png')
    
    def Update(self, deltatime):
        for layer in self.mLayerArray:
            layer.mOffset+=Paras.BackgroundAnimationSpeed*deltatime
            if layer.mOffset>Paras.WINDOWHEIGHT:
                layer.mOffset=-2*Paras.WINDOWHEIGHT+layer.mOffset
    
    def Draw(self, surf):
        for layer in self.mLayerArray:
            self._DrawLayer(surf, layer)
        
    
    def _DrawLayer(self, surf, layer):
        img=pygame.transform.scale(layer.mImg,(Paras.WINDOWWIDTH, Paras.WINDOWHEIGHT))
        img_width, img_height=img.get_size()
        img_x=(Paras.WINDOWWIDTH-img_width)//2
        img_y=(Paras.WINDOWHEIGHT-img_height)//2
        img_y+=layer.mOffset
        surf.blit(img, (img_x, img_y))