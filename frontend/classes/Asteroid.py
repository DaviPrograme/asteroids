from random import randint
import pygame
import os
from math import cos, radians, sin


class Asteroid(pygame.sprite.Sprite):
    asteroids = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/asteroides/"
        self.image = pygame.image.load(self._path + "pedra_grande.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.position = pygame.Vector2(randint(0, 1260), randint(0, 760))
        self.speed = 100
        self.angle = randint(0, 360)
        self.rect = self.image.get_rect(center=self.position)

    @classmethod
    def load_asteroid(cls):
        while len(cls.asteroids) < 5:
            cls.asteroids.append(Asteroid())

    def move(self, dt):
        move_ang = radians(self.angle)
        if move_ang > 0 or move_ang < 180:
            self.position.y += self.speed * sin(move_ang) * dt
            self.position.x -= self.speed * cos(move_ang) * dt
        else:
            self.position.y -= self.speed * sin(move_ang) * dt
            self.position.x += self.speed * cos(move_ang) * dt

        # self.rect.center = (int(self.position[0] - self.image.get_width()/2), int(self.position[1] - self.image.get_height()/2))* dt

        self.rect.center = (int(self.position[0]), int(self.position[1]))

    @classmethod
    def update_asteroid(cls, dt):
        cls.load_asteroid()
        for asteroid in cls.asteroids:
            asteroid.move(dt)
            if asteroid.position[0] < 0 or asteroid.position[0] > 1280 or asteroid.position[1] < 0 or asteroid.position[1] > 720:
                cls.asteroids.remove(asteroid)