from classes.Game import Game 
import pygame_menu

if __name__ == "__main__":
    def run_game(game):
        game.run().quit()


    game = Game()
    menu = pygame_menu.Menu('Asteroids', 400, 300, theme=pygame_menu.themes.THEME_DARK)
    menu.add.text_input('Name :', default='John Doe')
    menu.add.button('Play', run_game, game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(game._surface)
