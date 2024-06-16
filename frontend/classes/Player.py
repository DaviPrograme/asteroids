from math import cos, radians, sin
import pygame
from classes.Nave import Nave
from classes.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x_init, y_init):
        pygame.sprite.Sprite.__init__(self)
        self._nave = Nave()
        self.image = self._nave.sprites["parado"]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(x_init, y_init)
        self._player_speed = 300
        self._rotation_speed = 2.0
        self._player_angle = 90.0
        self.rect = self.image.get_rect(center=self.pos)
        self._current_frame = 0
        self._frame_counter = 0
        self._current_time = 0
        self._animation_time = 0.095
        self.death = False


    def rotate_player(self, angle):
        self._player_angle += angle  # Update player angle
        if abs(self._player_angle) >= 360:
            self._player_angle = (self._player_angle) % 360
        self.image = pygame.transform.rotate(self.image, self._player_angle)  # Rotate player sprite

    def stoped(self):
        self.image = self._nave.sprites["parado90"]
        self.rotate_player(0)

    def shoot(self, dt):
        off_x = cos(radians(self._player_angle)) * self.image.get_width() /2
        off_y = sin(radians(self._player_angle)) * self.image.get_height() /2
        new_pos = pygame.Vector2(self.pos.x + off_x, self.pos.y - off_y)
        Bullet.load_bullet(new_pos, self._player_angle, dt)

    def movement(self, dt, keys):
        if keys[pygame.K_w]:
            self.image = self._nave.sprites["boost_duplo"]
            self.rotate_player(0)
            move_ang = radians(self._player_angle)
            self.pos.y -= self._player_speed * sin(move_ang) * dt
            self.pos.x += self._player_speed * cos(move_ang) * dt
        if keys[pygame.K_a]:
            self.image = self._nave.sprites["boost_right"]
            self.rotate_player(self._rotation_speed)
        if keys[pygame.K_d]:
            self.image = self._nave.sprites["boost_left"]
            self.rotate_player(-self._rotation_speed)
        self.rect.center = (self.pos[0] - self.image.get_width()/2, self.pos[1] - self.image.get_height()/2)

    def explode(self, dt):
        self._current_time += dt
        if self._current_time >= self._animation_time:
            self._current_time = 0
            self._frame_counter = (self._frame_counter + 1 )
        try:
            self.image = self._nave.sprites["explosao"][self._frame_counter]
            self.rotate_player(0)
            self.death = True
            return True
        except:
            pass
        return False

