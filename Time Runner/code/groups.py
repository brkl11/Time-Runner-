import pygame
from settings import *

class AllSprites(pygame.sprite.Group):
    """
    Custom sprite group to handle drawing with an offset for a moving effect.
    """

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        """
        Draw all sprites with an offset based on the target position.

        Args:
            target_pos (tuple): The position of the target (e.g., player) to center the screen around.
        """
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)