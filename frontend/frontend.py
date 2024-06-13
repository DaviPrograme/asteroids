import pygame
import sys
sys.path.append("../frontend")

from classes.Nave import Nave
from classes.Player import Player

def rotate_player(player, angle):
    player._player_angle += angle  # Update player angle
    player._player_image = pygame.transform.rotate(player._player_image, player._player_angle)  # Rotate player sprite
    
    # player.
if __name__ == "__main__":


    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    nave = Nave()
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    player = Player(nave.sprites["parado"])
    player.player_pos = player_pos
    player._player_angle
  
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(0)
        # screen.blit(nave.sprite, (0,0), (0,0, 70, 70))

        # pygame.draw.circle(screen, "red", player_pos, 40)
        
        # screen.blit(player._player_image, player_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_w]:
            player._player_image = nave.sprites["boost_duplo"]
            player._player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            pass
            # player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player._player_image = nave.sprites["boost_left"]
            rotate_player(player, player._rotation_speed)
        if keys[pygame.K_d]:
            player._player_image = nave.sprites["boost_right"]
            rotate_player(player, -player._rotation_speed)

        player._player_rect.center = (player._player_pos[0]-player._player_image.get_width()/2, player._player_pos[1]-player._player_image.get_height()/2)
        # Blit the rotated image
        screen.blit(player._player_image, player._player_rect.center)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()