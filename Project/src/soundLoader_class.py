import pygame

class SoundLoader:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SoundLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.loaded_sounds = {}

    def load_sound(self, sound_path):
        if sound_path not in self.loaded_sounds:
            self.loaded_sounds[sound_path] = pygame.mixer.Sound(sound_path)
        return self.loaded_sounds[sound_path]