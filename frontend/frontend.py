import pygame
import sys
from classes.Player import Player

    
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

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        player.movement(dt, keys)
        # Blit the rotated image
        screen.blit(player._player_image, player._player_rect.center)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()