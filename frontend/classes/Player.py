from cairo import Surface
import pygame


class Player():
    def __init__(self, image):
        self._player_og_image = image
        self._player_image = image
        self._player_pos = pygame.Vector2()
        self._player_speed = 300
        self._rotation_speed = 2.0
        self._player_angle = 0.0
        self._player_rect = image.get_rect(center=self._player_pos)

        # self._player_rect.center = self._player_pos
        # self._player_sprite = nave.sprites["parado"]



    # def movement(self, dt):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_w]:
    #         self._player_pos.y -= self._player_speed * dt
    #     if keys[pygame.K_s]:
    #         self._player_pos.y += self._player_speed * dt
    #     if keys[pygame.K_a]:
    #         self.rotate_player(self._rotation_speed, "left")
    #     if keys[pygame.K_d]:
    #         self.rotate_player(-self._rotation_speed, "right")

    @property
    def player_pos(self):
        return self._player_pos

    @player_pos.setter
    def player_pos(self, novo_pos):
        self._player_pos = novo_pos

    # @property
    # def player_sprite(self):
    #     return self._player_sprite

    # @player_sprite.setter
    # def player_sprite(self, novo_sprite):
    #     self._player_sprite = novo_sprite