import pygame

class UI:
    def __init__(self, game):
        self.mGame=game
        self.font = pygame.font.Font(None, 36)
    def Draw(self, surf):
        level_text = self.font.render(f"Level: {self.mGame.mLevel}", True, (255, 255, 255))
        text_width, text_height = level_text.get_size()
        x = surf.get_width() - text_width - 10
        y = 10
        surf.blit(level_text, (x, y))