		# self._font = pygame.font.SysFont(self._ttf, 24)
import pygame
import os

class Text():
	def __init__(self, text, pos_x, pos_y):
		"""__init__
			Método construtor da classe Text
			:param self: Classe Text
			:param text: Texto
			:param pos_x: Posição x
			:param pos_y: Posição y
		"""
		self._path = os.path.abspath(os.path.dirname(__file__)) + "/../../frontend/sprites/"
		self._font = pygame.font.Font(self._path + "A-cuchillada-font-ffp.ttf", 24)
		self.pos  = pygame.Vector2(pos_x, pos_y)
		self.image = self.render(text, (255, 255, 255))
		self.rect = self.image.get_rect(center=self.pos)
	
	def render(self, text, color):
		"""render
			Método que renderiza o texto
			:param self: Classe Text
			:param text: Texto
			:param color: Cor
		"""
		return self._font.render(text, True, color)