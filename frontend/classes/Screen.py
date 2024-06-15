import pygame

class Screen():
    def __init__(self, window_heght, window_width):
        self._screen = pygame.display.set_mode((window_heght, window_width))
    
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