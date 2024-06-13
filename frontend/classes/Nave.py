import pygame
import os

class Nave():
    def __init__(self):
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/nave/"
        self._sprite = pygame.image.load(self._path + "nave_sem_boost.png").convert_alpha()
        self.sprites = {
            "parado" : pygame.image.load(self._path + "nave_sem_boost.png").convert_alpha(),
            "boost_left" : pygame.image.load(self._path + "nave_boost_left.png").convert_alpha(),
            "boost_right" : pygame.image.load(self._path + "nave_boost_right.png").convert_alpha(),
            "boost_duplo" : pygame.image.load(self._path + "nave_boost_duplo.png").convert_alpha(),
            "explosao" : [
                pygame.image.load(self._path + "nave_explosao_1.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_2.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_3.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_4.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_5.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_6.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_7.png").convert_alpha(),
            ]
        }

    @property
    def sprite(self):
        return self._sprite
    
    @sprite.setter
    def sprite(self, novo_sprite):
        self._sprite = novo_sprite