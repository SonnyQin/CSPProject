import pygame
import math

#Singleton
class ImageLoader:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.loaded_images = {}

    def load_image(self, image_path):
        if image_path not in self.loaded_images:
            self.loaded_images[image_path] = pygame.image.load(image_path)
        return self.loaded_images[image_path]

def DrawImage(surf, img, pos, rotation, scale=1.0):
    img_x, img_y = img.get_size()
    new_x = int(img_x * scale)
    new_y = int(img_y * scale)
    img_scaled = pygame.transform.scale(img, (new_x, new_y))
    img_rotated = pygame.transform.rotate(img_scaled, math.degrees(rotation))
    rot_x, rot_y = img_rotated.get_size()

    draw_x = pos.x - rot_x / 2
    draw_y = pos.y - rot_y / 2

    surf.blit(img_rotated, (draw_x, draw_y))