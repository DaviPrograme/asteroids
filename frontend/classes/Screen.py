import pygame

class Screen():
    def __init__(self, window_heght, window_width):
        self.is_player_colided = False
        self._screen = pygame.display.set_mode((window_heght, window_width))
    
    def update_collisions(self, player, asteroide_group, bullets_group):
        self.is_player_colided = True if len(pygame.sprite.spritecollide(player, asteroide_group, False, pygame.sprite.collide_mask)) > 0 else False
        for bullet in bullets_group:
            for asteroid in asteroide_group:
                if pygame.sprite.collide_mask(bullet, asteroid):
                    asteroide_group.remove(asteroid)
                    bullets_group.remove(bullet)

    def render(self, objects):
        self._screen.fill(0)
        for obj in objects:
            self._screen.blit(obj.image, obj.rect.center)

        # flip() the display to put your work on screen
        pygame.display.flip()

    @property
    def width(self):
        return self._screen.get_width()

    @property
    def height(self):
        return self._screen.get_height()