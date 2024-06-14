import pygame
import os

class Nave():
    def __init__(self):
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/nave/"
        # self._sprite = pygame.image.load(self._path + "nave_sem_boost90.png").convert_alpha()
        self._sprites = {
            "parado" : pygame.image.load(self._path + "nave_sem_boost.png").convert_alpha(),
            "parado90" : pygame.image.load(self._path + "nave_sem_boost90.png").convert_alpha(),
            "boost_left" : pygame.image.load(self._path + "nave_boost_left90.png").convert_alpha(),
            "boost_right" : pygame.image.load(self._path + "nave_boost_right90.png").convert_alpha(),
            "boost_duplo" : pygame.image.load(self._path + "nave_boost_duplo90.png").convert_alpha(),
            "explosao" : [
                pygame.image.load(self._path + "nave_explosao_190.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_290.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_390.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_490.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_590.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_690.png").convert_alpha(),
                pygame.image.load(self._path + "nave_explosao_790.png").convert_alpha(),
            ]
        }

    @property
    def sprites(self):
        return self._sprites
    
    # @sprites.setter
    # def sprites(self, novo_sprite):
    #     self.sprites = novo_sprite