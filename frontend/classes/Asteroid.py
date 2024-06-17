from random import randint
import pygame
import os
from math import cos, radians, sin


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
    def load_asteroid(cls, ):
        while len(cls.asteroids) < 5:
            cls.asteroids.append(Asteroid())

    def asteroid_initial_position(self):
        self.id = Asteroid.id
        Asteroid.id += 1
        if self.id % 2 == 0:
            self.pos = pygame.Vector2(randint(0, 1280), 780)
            self.angle = randint(180, 360)
        else:
            self.pos = pygame.Vector2(randint(0, 1280), -30)
            self.angle = randint(0, 180)

    def image_select(self, size):
        if size == 3:
            return pygame.image.load(self._path + "pedra_grande.png").convert_alpha()
        elif size == 2:
            return pygame.image.load(self._path + "pedra_media.png").convert_alpha()
        elif size == 1:
            return pygame.image.load(self._path + "pedra_pequena.png").convert_alpha()

    def move(self, dt):
        move_ang = radians(self.angle)
        if move_ang > 0 or move_ang < 180:
            self.pos.y += self.speed * sin(move_ang) * dt
            self.pos.x -= self.speed * cos(move_ang) * dt
        else:
            self.pos.y -= self.speed * sin(move_ang) * dt
            self.pos.x += self.speed * cos(move_ang) * dt
        self.rect.center = (int(self.pos[0]), int(self.pos[1]))

    def explode(self):
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
        cls.load_asteroid()
        for asteroid in cls.asteroids:
            asteroid.move(dt)
            if asteroid.pos[0] < -50 or asteroid.pos[0] > 1330 or asteroid.pos[1] < -50 or asteroid.pos[1] > 830:
                cls.asteroids.remove(asteroid)