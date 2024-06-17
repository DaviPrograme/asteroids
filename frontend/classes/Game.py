import pygame
from classes.Player import Player
from classes.Bullet import Bullet
from classes.Asteroid import Asteroid
from classes.Screen import Screen

class Game():
    def __init__(self):
        pygame.init()
        self._window_height = 1280
        self._window_width = 720
        self._screen = Screen(self._window_height, self._window_width)
        self._player = Player(self._window_width / 2, self._window_height / 2)
        self._clock = pygame.time.Clock()
        self._running = True
        self._dt = 0

    def run(self):
        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if not self._player.death and event.type == pygame.KEYUP:
                    self._player.stoped()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                    if not self._player.death and event.key == pygame.K_SPACE:
                        self._player.shoot(self._dt)

            self._screen.render([*Bullet.bullets, *Asteroid.asteroids, self._player])
            if not self._screen.is_player_colided and not self._screen.update_collisions(self._player, Asteroid.asteroids, Bullet.bullets):
                self._player.movement(self._dt, pygame.key.get_pressed())
                Bullet.update_bullets(self._dt)
                Asteroid.update_asteroid(self._dt, self._screen.width, self._screen.height)
            else:
                self._player.explode(self._dt)

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self._dt = self._clock.tick(60) / 1000
        pygame.quit()