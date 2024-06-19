import pygame
from classes.Bullet import Bullet

class Screen():
    def __init__(self, window_heght, window_width):
        self.is_player_colided = False
        self._screen = pygame.display.set_mode((window_heght, window_width))

    def checking_collision_between_player_and_asteroids(self, player, asteroids):
        asteroids_collided_with_player = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_mask)
        for asteroid_collided in asteroids_collided_with_player:
            asteroids.remove(asteroid_collided)
        return True if len(asteroids_collided_with_player) > 0 else False

    def checking_collision_between_bullets_and_asteroids(self, bullets, asteroids, update_score):
        for bullet in bullets:
            asteroids_collided_with_bullet = pygame.sprite.spritecollide(bullet, asteroids, False, pygame.sprite.collide_mask)
            if asteroids_collided_with_bullet :
                bullets.remove(bullet)
            for asteroid in asteroids_collided_with_bullet:
                update_score(asteroid)
                asteroid.explode()


    def update_collisions(self, player, asteroide_group, bullets_group, update_score):
        self.is_player_colided = self.checking_collision_between_player_and_asteroids(player, asteroide_group)
        self.checking_collision_between_bullets_and_asteroids(bullets_group, asteroide_group, update_score)
        return self.is_player_colided

    def off_screen(self, x, y):
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