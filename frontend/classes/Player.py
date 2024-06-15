from math import cos, radians, sin
import pygame
from classes.Nave import Nave


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._nave = Nave()
        self.image = self._nave.sprites["parado"]
        self.mask = pygame.mask.from_surface(self.image)
        self._player_pos = pygame.Vector2()
        self._player_speed = 300
        self._rotation_speed = 2.0
        self._player_angle = 90.0
        self.rect = self.image.get_rect(center=self._player_pos)
        self._current_frame = 0
        self._frame_counter = 0
        self._current_time = 0
        self._animation_time = 0.095
        self.death = False
        self.radius = 35


    def rotate_player(self, angle):
        self._player_angle += angle  # Update player angle
        if abs(self._player_angle) >= 360:
            self._player_angle = (self._player_angle) % 360
        self.image = pygame.transform.rotate(self.image, self._player_angle)  # Rotate player sprite

    def stoped(self):
        self.image = self._nave.sprites["parado90"]
        self.rotate_player(0)


    def movement(self, dt, keys):
        if keys[pygame.K_w]:
            self.image = self._nave.sprites["boost_duplo"]
            self.rotate_player(0)
            move_ang = radians(self._player_angle)
            self._player_pos.y -= self._player_speed * sin(move_ang) * dt
            self._player_pos.x += self._player_speed * cos(move_ang) * dt
        if keys[pygame.K_a]:
            self.image = self._nave.sprites["boost_right"]
            self.rotate_player(self._rotation_speed)
        if keys[pygame.K_d]:
            self.image = self._nave.sprites["boost_left"]
            self.rotate_player(-self._rotation_speed)
        self.rect.center = (self._player_pos[0] - self.image.get_width()/2, self._player_pos[1] - self.image.get_height()/2)

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

    @property
    def player_pos(self):
        return self._player_pos

    @player_pos.setter
    def player_pos(self, novo_pos):
        self._player_pos = novo_pos

class Bullet():
    bullets = []
    def __init__(self, player_x, player_y, player_angle):
        # self.image = pygame.image.load("frontend/sprites/nave/tiro.png").convert_alpha()
        self.image = pygame.transform.rotate(pygame.image.load("frontend/sprites/nave/tiro.png").convert_alpha(), player_angle)  # Rotate bullet sprite
        self._bullet_pos = pygame.Vector2(player_x, player_y)
        self._bullet_angle = player_angle
        self._bullet_speed = 600
        self.rect = self.image.get_rect(center=self._bullet_pos)

    @classmethod
    def load_bullet(cls, bullet_pos, bullet_angle, dt):
        gun_x = bullet_pos[0]
        gun_y = bullet_pos[1]
        Bullet.bullets.append(Bullet(gun_x, gun_y, bullet_angle))

    def move(self, dt):
        move_ang = radians(self.bullet_angle)
        self._bullet_pos.y -= self._bullet_speed * sin(move_ang) * dt
        self._bullet_pos.x += self._bullet_speed * cos(move_ang) * dt
        self.rect.center = (int(self._bullet_pos[0] - self.image.get_width()/2), int(self._bullet_pos[1] - self.image.get_height()/2))
    
    @classmethod
    def update_bullets(cls, dt):
        for bullet in cls.bullets:
            if bullet.bullet_pos[0] < 0 or bullet.bullet_pos[0] > 1280 or bullet.bullet_pos[1] < 0 or bullet.bullet_pos[1] > 720:
                cls.bullets.remove(bullet)
            else: 
                bullet.move(dt)

    @property
    def bullet_pos(self):
        return self._bullet_pos

    @bullet_pos.setter
    def bullet_pos(self, novo_pos):
        self._bullet_pos = novo_pos

    @property
    def bullet_angle(self):
        return self._bullet_angle

    @bullet_angle.setter
    def bullet_angle(self, novo_ang):
        self._bullet_angle = novo_ang