import pygame
import os
import math


class Asteroid():
    def __init__(self):
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/asteroides/"
        self.image = pygame.image.load(self._path + "pedra_grande.png").convert_alpha()
        self.position = pygame.Vector2(100,100)
        self.asteroid_rect = self.image.get_rect(center=self.position)
        self.radius = 40

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj._player_pos)
        return distance < self.radius + other_obj.radius