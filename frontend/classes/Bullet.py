from math import cos, radians, sin
import pygame

class Bullet():
    bullets = []
    def __init__(self, player_x, player_y, player_angle):
        """__init__ 
            Método construtor da classe Bullet
            :param self: Classe Bullet
            :param player_x: Posição x do jogador
            :param player_y: Posição y do jogador
            :param player_angle: Ângulo do jogador
        """
        self.image = pygame.transform.rotate(pygame.image.load("frontend/sprites/nave/tiro.png").convert_alpha(), player_angle)  # Rotate bullet sprite
        self.pos = pygame.Vector2(player_x, player_y)
        self._bullet_angle = player_angle
        self._bullet_speed = 600
        self.rect = self.image.get_rect(center=self.pos)
        self.is_off_screen = False

    @classmethod
    def load_bullet(cls, bullet_pos, bullet_angle, dt):
        """load_bullet 
            Método que carrega a bala na tela
            :param cls: Classe Bullet
            :param bullet_pos: Posição da bala
            :param bullet_angle: Ângulo da bala
            :param dt: Tempo
        """
        gun_x = bullet_pos[0]
        gun_y = bullet_pos[1]
        Bullet.bullets.append(Bullet(gun_x, gun_y, bullet_angle))

    def move(self, dt):
        """move 
            Método que move a bala
            :param self: Classe Bullet
            :param dt: Tempo
        """
        move_ang = radians(self._bullet_angle)
        self.pos.y -= self._bullet_speed * sin(move_ang) * dt
        self.pos.x += self._bullet_speed * cos(move_ang) * dt
        self.rect.center = (int(self.pos[0] - self.image.get_width()/2), int(self.pos[1] - self.image.get_height()/2))
    
    @classmethod
    def update_bullets(cls, dt):
        """update_bullets 
            Método que atualiza a posição da bala
            :param cls: Classe Bullet
            :param dt: Tempo
        """
        for bullet in cls.bullets:
            if bullet.pos[0] < 0 or bullet.pos[0] > 1280 or bullet.pos[1] < 0 or bullet.pos[1] > 720:
                cls.bullets.remove(bullet)
            else: 
                bullet.move(dt)
