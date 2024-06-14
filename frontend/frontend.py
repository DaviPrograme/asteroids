from math import sin, cos, radians
import pygame
from classes.Player import Bullet, Player
    
if __name__ == "__main__":

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player = Player()
    player.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    player._player_angle
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                player.stoped()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    off_x = cos(radians(player._player_angle)) * player._player_image.get_width() /2
                    off_y = sin(radians(player._player_angle)) * player._player_image.get_height() /2
                    new_pos = pygame.Vector2(player._player_pos.x + off_x, player._player_pos.y + off_y)
                    Bullet.load_bullet(new_pos, player._player_angle, dt)
                    print(len(Bullet.bullets))

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(0)
        keys = pygame.key.get_pressed()
        player.movement(dt, keys)
        Bullet.update_bullets(dt)
        for bullet in Bullet.bullets:
            screen.blit(bullet._bullet_image, bullet._bullet_rect.center)
        # Blit the rotated image
        screen.blit(player._player_image, player._player_rect.center)
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()