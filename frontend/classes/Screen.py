import pygame
from classes.Bullet import Bullet

class Screen():
    def __init__(self, window_heght, window_width):
        """__init__
            Método construtor da classe Screen
            :param self: Classe Screen
            :param window_heght: Altura da janela
            :param window_width: Largura da janela
        """
        self.is_player_colided = False
        self._screen = pygame.display.set_mode((window_heght, window_width))

    def checking_collision_between_player_and_asteroids(self, player, asteroids):
        """checking_collision_between_player_and_asteroids
            Método que verifica se houve colisão entre o jogador e os asteroides
            :param self: Classe Screen
            :param player: Jogador
            :param asteroids: Asteroides
        """
        asteroids_collided_with_player = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_mask)
        for asteroid_collided in asteroids_collided_with_player:
            asteroids.remove(asteroid_collided)
        return True if len(asteroids_collided_with_player) > 0 else False

    def checking_collision_between_bullets_and_asteroids(self, bullets, asteroids, update_score):
        """checking_collision_between_bullets_and_asteroids
            Método que verifica se houve colisão entre os tiros e os asteroides
            :param self: Classe Screen
            :param bullets: Tiros
            :param asteroids: Asteroides
            :param update_score: Função que atualiza a pontuação
        """
        for bullet in bullets:
            asteroids_collided_with_bullet = pygame.sprite.spritecollide(bullet, asteroids, False, pygame.sprite.collide_mask)
            if asteroids_collided_with_bullet :
                bullets.remove(bullet)
            for asteroid in asteroids_collided_with_bullet:
                update_score(asteroid)
                asteroid.explode()


    def update_collisions(self, player, asteroide_group, bullets_group, update_score):
        """update_collisions
            Método que atualiza as colisões
            :param self: Classe Screen
            :param player: Jogador
            :param asteroide_group: Grupo de asteroides
            :param bullets_group: Grupo de tiros
            :param update_score: Função que atualiza a pontuação
        """
        self.is_player_colided = self.checking_collision_between_player_and_asteroids(player, asteroide_group)
        self.checking_collision_between_bullets_and_asteroids(bullets_group, asteroide_group, update_score)
        return self.is_player_colided

    def off_screen(self, x, y):
        """off_screen
            Método que verifica se o objeto está fora da tela
            :param self: Classe Screen
            :param x: Posição x
            :param y: Posição y
        """
        if x < 0:
            x += self.width
        if x > self.width:
            x -= self.width
        if y < 0 :
            y += self.height
        if y > self.height:
            y -= self.height
        return pygame.Vector2(x, y)

    def render(self, objects):
        """render
            Método que renderiza os objetos na tela
            :param self: Classe Screen
            :param objects: Objetos
        """
        self._screen.fill(0)
        for obj in objects:
            if not isinstance(obj, Bullet):
                obj.pos = self.off_screen(obj.pos[0], obj.pos[1])
            self._screen.blit(obj.image, obj.rect.center)
        # flip() the display to put your work on screen
        pygame.display.flip()

    @property
    def width(self):
        return self._screen.get_width()

    @property
    def height(self):
        return self._screen.get_height()