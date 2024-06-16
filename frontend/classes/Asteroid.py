from random import randint
import pygame
import os
from math import cos, radians, sin


class Asteroid(pygame.sprite.Sprite):
    asteroids = []
    id = 0
    def __init__(self, height, width):
        pygame.sprite.Sprite.__init__(self)
        self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/asteroides/"
        self.image = pygame.image.load(self._path + "pedra_grande.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.asteroid_initial_position()
        self.speed = 100
        self.rect = self.image.get_rect(center=self.position)

    @classmethod
    def load_asteroid(cls, height, width):
        print(len(cls.asteroids))
        while len(cls.asteroids) < 5:
            cls.asteroids.append(Asteroid(height, width))

    def asteroid_initial_position(self):
        self.id = Asteroid.id
        Asteroid.id += 1
        if self.id % 2 == 0:
            self.position = pygame.Vector2(randint(0, 1280), 780)
            self.angle = randint(180, 360)
        else:
            self.position = pygame.Vector2(randint(0, 1280), -30)
            self.angle = randint(0, 180)


    def move(self, dt):
        move_ang = radians(self.angle)
        if move_ang > 0 or move_ang < 180:
            self.position.y += self.speed * sin(move_ang) * dt
            self.position.x -= self.speed * cos(move_ang) * dt
        else:
            self.position.y -= self.speed * sin(move_ang) * dt
            self.position.x += self.speed * cos(move_ang) * dt
        self.rect.center = (int(self.position[0]), int(self.position[1]))

    @classmethod
    def update_asteroid(cls, dt, height, width):
        cls.load_asteroid(height, width)
        for asteroid in cls.asteroids:
            asteroid.move(dt)
            if asteroid.position[0] < -50 or asteroid.position[0] > 1330 or asteroid.position[1] < -50 or asteroid.position[1] > 830:
                cls.asteroids.remove(asteroid)