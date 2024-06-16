import pygame
from classes.Bullet import Bullet

class Screen():
    def __init__(self, window_heght, window_width):
        self.is_player_colided = False
        self._screen = pygame.display.set_mode((window_heght, window_width))
    
    def update_collisions(self, player, asteroide_group, bullets_group):
        #checking the collision between the player and the asteroids
        asteroids_collided_with_player = pygame.sprite.spritecollide(player, asteroide_group, False, pygame.sprite.collide_mask)
        self.is_player_colided = True if len(asteroids_collided_with_player) > 0 else False
        for asteroid_collided in asteroids_collided_with_player:
            asteroide_group.remove(asteroid_collided)

        #checking the collision between bullets and asteroids
        for bullet in bullets_group:
            for asteroid in asteroide_group:
                if pygame.sprite.collide_mask(bullet, asteroid):
                    asteroide_group.remove(asteroid)
                    bullets_group.remove(bullet)
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