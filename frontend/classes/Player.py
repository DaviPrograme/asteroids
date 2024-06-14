from math import cos, radians, sin
import pygame
from classes.Nave import Nave


class Player():
    def __init__(self):
        self._nave = Nave()
        self._player_image = self._nave.sprites["parado"]
        self._player_pos = pygame.Vector2()
        self._player_speed = 300
        self._rotation_speed = 2.0
        self._player_angle = 90.0
        self._player_rect = self._player_image.get_rect(center=self._player_pos)

    def rotate_player(self, angle):
        if abs(self._player_angle + angle) >= 360:
            self._player_angle = (self._player_angle + angle) % 360
        else:
            self._player_angle += angle  # Update player angle
        self._player_image = pygame.transform.rotate(self._player_image, self._player_angle)  # Rotate player sprite

    def stoped(self):
        self._player_image = self._nave.sprites["parado90"]
        self.rotate_player(0)


    def movement(self, dt, keys):
        if keys[pygame.K_w]:
            self._player_image = self._nave.sprites["boost_duplo"]
            self.rotate_player(0)
            move_ang = radians(self._player_angle)
            self._player_pos.y -= self._player_speed * sin(move_ang) * dt
            self._player_pos.x += self._player_speed * cos(move_ang) * dt
            print(self._player_angle)
        if keys[pygame.K_a]:
            self._player_image = self._nave.sprites["boost_right"]
            self.rotate_player(self._rotation_speed)
        if keys[pygame.K_d]:
            self._player_image = self._nave.sprites["boost_left"]
            self.rotate_player(-self._rotation_speed)
        self._player_rect.center = (self._player_pos[0] - self._player_image.get_width()/2, self._player_pos[1] - self._player_image.get_height()/2)


    @property
    def player_pos(self):
        return self._player_pos

    @player_pos.setter
    def player_pos(self, novo_pos):
        self._player_pos = novo_pos