import pygame_menu
from classes.Game import Game

class Menu():
    def __init__(self):
        """__init__ 
            Método construtor da classe Menu
            :param self: Classe Menu
        """
        self._game = Game()
        self._menu = pygame_menu.Menu('Asteroids', 400, 300, theme=pygame_menu.themes.THEME_DARK)
        self._menu.add.text_input('Name :', default='John Doe', onchange = self._game.set_player_name)
        self._menu.add.button('Play', self._game.run)
        self._menu.add.button('Quit', pygame_menu.events.EXIT)
    
    def run(self):
        """run 
            Método que roda o menu
            :param self: Classe Menu
        """
        self._menu.mainloop(self._game._surface)