from math import sin, cos, radians
from time import sleep
import pygame
from classes.Player import Bullet, Player
from classes.Asteroid import Asteroid
from classes.Screen import Screen



if __name__ == "__main__":

    # pygame setup
    pygame.init()
    screen = Screen(1280, 720)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player = Player()
    asteroid = Asteroid()
    player.player_pos = pygame.Vector2(screen.width / 2, screen.height / 2)
    player._player_angle

    asteroide_group = pygame.sprite.Group()
    asteroide_group.add(asteroid)
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not player.death and event.type == pygame.KEYUP:
                player.stoped()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if not player.death and event.key == pygame.K_SPACE:
                    off_x = cos(radians(player._player_angle)) * player.image.get_width() /2
                    off_y = sin(radians(player._player_angle)) * player.image.get_height() /2
                    new_pos = pygame.Vector2(player._player_pos.x + off_x, player._player_pos.y - off_y)
                    Bullet.load_bullet(new_pos, player._player_angle, dt)

        # fill the screen with a color to wipe away anything from last frame
        keys = pygame.key.get_pressed()
        screen.render([*Bullet.bullets, asteroid, player])

        is_collision = pygame.sprite.spritecollide(player, asteroide_group, False, pygame.sprite.collide_mask)
        if is_collision :
            player.explode(dt)
        else:
            player.movement(dt, keys)
            Bullet.update_bullets(dt)

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()