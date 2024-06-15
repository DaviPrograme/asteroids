import pygame
import os
import math


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/asteroides/"
        self.image = pygame.image.load(self._path + "pedra_grande.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.position = pygame.Vector2(100,100)
        self.rect = self.image.get_rect(center=self.position)