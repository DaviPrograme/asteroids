from time import sleep
import os
import sys
import pygame
from classes.Player import Player
from classes.Bullet import Bullet
from classes.Asteroid import Asteroid
from classes.Screen import Screen
from classes.Text import Text
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../../backend/postgres")
from db.query import update_db

class Game():
    def __init__(self):
        """__init__ 
            Método construtor da classe Game
            :param self: Classe Game
        """
        self._lib = pygame.init()
        self._window_height = 1280
        self._window_width = 720
        self._screen = Screen(self._window_height, self._window_width)
        self._player = Player(self._window_width / 2, self._window_height / 2)
        self._clock = pygame.time.Clock()
        self._running = True
        self._dt = 0
        self._surface = pygame.display.get_surface()
        self._health = 2
        self._score = 0
        self._player_name = "John Doe"

    def set_player_name(self, name):
        """set_player_name
            Método que define o nome do jogador
            :param self: Classe Game
            :param name: Nome do jogador
        """
        self._player_name = name

    def player_score(self, asteroid):
        """player_score
            Método que calcula a pontuação do jogador
            :param self: Classe Game
            :param asteroid: Asteroide
        """
        if asteroid.size == 3:
            self._score += 10
        elif asteroid.size == 2:
            self._score += 20
        elif asteroid.size == 1:
            self._score += 30

    def run(self):
        """run 
            Método que roda o jogo
            :param self: Classe Game
        """
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
            
            health_text = Text(f"Health: {self._health + 1}", 30, 30)
            score_text = Text(f"Score: {self._score}", 1000, 30)
            name_text = Text(self._player_name, 550, 30)

            self._screen.render([*Bullet.bullets, *Asteroid.asteroids, self._player, health_text, score_text, name_text])
            if not self._screen.is_player_colided and not self._screen.update_collisions(self._player, Asteroid.asteroids, Bullet.bullets, self.player_score):
                self._player.movement(self._dt, pygame.key.get_pressed())
                Bullet.update_bullets(self._dt)
                Asteroid.update_asteroid(self._dt)
            else:
                if not self._player.explode(self._dt) and self._health >= 0:
                    self._screen.is_player_colided = False
                    self._health -= 1
                    self._player.reset() 
                if self._health < 0:
                    self._running = False

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self._dt = self._clock.tick(60) / 1000
        print(f"Game Over! Your score was: {self._score}")
        self._screen.render([Text(f"Game Over! Your score was: {self._score}", 400, 300)])
        update_db(self._player_name, self._score)
        sleep(5)
        sys.exit()
