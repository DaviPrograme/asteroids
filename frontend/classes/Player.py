from math import cos, radians, sin
import pygame
from classes.Nave import Nave
from classes.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x_init, y_init):
        """__init__ 
            Método construtor da classe Player
            :param self: Classe Player
            :param x_init: Posição x inicial
            :param y_init: Posição y inicial
        """
        pygame.sprite.Sprite.__init__(self)
        self._nave = Nave()
        self.image = self._nave.sprites["parado"]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(x_init, y_init)
        self._acceleration = 3
        self._max_speed = 500
        self._player_speed = 0
        self._rotation_speed = 2.0
        self._player_angle = 90.0
        self._directional_angle_speed = self._player_angle 
        self.rect = self.image.get_rect(center=self.pos)
        self._current_frame = 0
        self._frame_counter = 0
        self._current_time = 0
        self._animation_time = 0.095
        self.death = False
        self._score = 0

    def reset(self):
        """reset 
            Método que reseta o jogador
            :param self: Classe Player
        """
        self._player_speed = 0
        # self._player_angle = 90.0
        # self._directional_angle_speed = self._player_angle
        self._current_frame = 0
        self._frame_counter = 0
        self._current_time = 0
        self.death = False
        self.image = self._nave.sprites["parado"]
        # self._score = 0

    def rotate_player(self, angle):
        """rotate_player
            Método que rotaciona o jogador
            :param self: Classe Player
            :param angle: Ângulo de rotação
        """
        self._player_angle += angle  # Update player angle
        if abs(self._player_angle) >= 360:
            self._player_angle = (self._player_angle) % 360
        self.image = pygame.transform.rotate(self.image, self._player_angle)  # Rotate player sprite

    def stoped(self):
        """stoped 
            Método que para o jogador
            :param self: Classe Player
        """
        self.image = self._nave.sprites["parado90"]
        self.rotate_player(0)

    def shoot(self, dt):
        """shoot
            Método que faz o jogador atirar
            :param self: Classe Player
            :param dt: Tempo
        """
        off_x = cos(radians(self._player_angle)) * self.image.get_width() /2
        off_y = sin(radians(self._player_angle)) * self.image.get_height() /2
        new_pos = pygame.Vector2(self.pos.x + off_x, self.pos.y - off_y)
        Bullet.load_bullet(new_pos, self._player_angle, dt)

    def apply_acceleration(self):
        """apply_acceleration
            Método que aplica a aceleração no jogador
            :param self: Classe Player
        """
        self._player_speed = self._max_speed if self._player_speed + self._acceleration >= self._max_speed else self._player_speed + self._acceleration

    def apply_slowdown(self, delta):
        """apply_slowdown
            Método que aplica a desaceleração no jogador
            :param self: Classe Player
            :param delta: Delta
        """
        self._player_speed = 0 if self._player_speed - delta <= 0 else self._player_speed - delta

    def update_directional_angle_speed(self):
        """update_directional_angle_speed
            Método que atualiza a direção do jogador
            :param self: Classe Player
        """
        self._directional_angle_speed = self._player_angle if self._player_speed <= 100 else self._directional_angle_speed

    def movement(self, dt, keys):
        """movement
            Método que controla o movimento do jogador
            :param self: Classe Player
            :param dt: Tempo
            :param keys: Teclas pressionadas
        """
        if keys[pygame.K_w]:
            self.image = self._nave.sprites["boost_duplo"]
            self.rotate_player(0)
            if self._player_angle != self._directional_angle_speed:
                self.apply_slowdown(self._acceleration)
                self.update_directional_angle_speed()
            else:
                self.apply_acceleration()
            self.rect.center = (self.pos[0] - self.image.get_width()/2, self.pos[1] - self.image.get_height()/2)
        else:
            self.apply_slowdown(1)
        if keys[pygame.K_a]:
            self.image = self._nave.sprites["boost_right"]
            self.rotate_player(self._rotation_speed)
        if keys[pygame.K_d]:
            self.image = self._nave.sprites["boost_left"]
            self.rotate_player(-self._rotation_speed)

        self.update_directional_angle_speed()
        move_ang = radians((self._directional_angle_speed))
        self.pos.y -= self._player_speed * sin(move_ang) * dt
        self.pos.x += self._player_speed * cos(move_ang) * dt
        self.rect.center = (self.pos[0] - self.image.get_width()/2, self.pos[1] - self.image.get_height()/2)

    def explode(self, dt):
        """explode
            Método que faz o jogador explodir
            :param self: Classe Player
            :param dt: Tempo
        """
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
            return False

