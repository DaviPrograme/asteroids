from random import randint
import pygame
import os
from math import cos, radians, sin


"""Asteroid 
    Classe que representa um asteroide no jogo
"""
class Asteroid(pygame.sprite.Sprite):
    asteroids = []
    id = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/asteroides/"
        self.size = 3
        self.image = self.image_select(self.size)
        self.mask = pygame.mask.from_surface(self.image)
        self.asteroid_initial_position()
        self.speed = 100
        self.rect = self.image.get_rect(center=self.pos)

    @classmethod
    def load_asteroid(cls):
        """load_asteroid 
            Método que carrega os asteroides na tela
            :param cls: Classe Asteroid
        """
        while len(cls.asteroids) < 5:
            cls.asteroids.append(Asteroid())

    def asteroid_initial_position(self):
        """asteroid_initial_position
            Método que define a posição inicial do asteroide
            :param self: Classe Asteroid
        """
        self.id = Asteroid.id
        Asteroid.id += 1
        if self.id % 2 == 0:
            self.pos = pygame.Vector2(randint(0, 1280), 780)
            self.angle = randint(180, 360)
        else:
            self.pos = pygame.Vector2(randint(0, 1280), -30)
            self.angle = randint(0, 180)

    def image_select(self, size):
        """image_select 
            Método que seleciona a imagem do asteroide de acordo com o seu tamanho
            :param self: Classe Asteroid
            :param size: Tamanho do asteroide
        """
        if size == 3:
            return pygame.image.load(self._path + "pedra_grande.png").convert_alpha()
        elif size == 2:
            return pygame.image.load(self._path + "pedra_media.png").convert_alpha()
        elif size == 1:
            return pygame.image.load(self._path + "pedra_pequena.png").convert_alpha()

    def move(self, dt):
        """move 
            Método que move o asteroide
            :param self: Classe Asteroid
            :param dt: Tempo
        """
        move_ang = radians(self.angle)
        if move_ang > 0 or move_ang < 180:
            self.pos.y += self.speed * sin(move_ang) * dt
            self.pos.x -= self.speed * cos(move_ang) * dt
        else:
            self.pos.y -= self.speed * sin(move_ang) * dt
            self.pos.x += self.speed * cos(move_ang) * dt
        self.rect.center = (int(self.pos[0]), int(self.pos[1]))

    def explode(self):
        """explode 
            Método que faz o asteroide explodir
            :param self: Classe Asteroid
        """
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid()
                asteroid.pos = self.pos
                asteroid.size = self.size - 1
                asteroid.image = asteroid.image_select(asteroid.size)
                asteroid.speed = self.speed + 10
                asteroid.angle = randint(0, 360)
                self.asteroids.append(asteroid)
        self.asteroids.remove(self)

    @classmethod
    def update_asteroid(cls, dt):
        """update_asteroid 
            Método que atualiza a posição dos asteroides
            :param cls: Classe Asteroid
            :param dt: Tempo
        """
        cls.load_asteroid()
        for asteroid in cls.asteroids:
            asteroid.move(dt)
            if asteroid.pos[0] < -50 or asteroid.pos[0] > 1330 or asteroid.pos[1] < -50 or asteroid.pos[1] > 830:
                cls.asteroids.remove(asteroid)