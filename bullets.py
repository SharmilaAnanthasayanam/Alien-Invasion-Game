import pygame
from pygame.sprite import Sprite

class Bullets(Sprite):
	"""To create a bullet and shoot it"""
	def __init__(self,ai_game):
		super().__init__()
		self.ai_screen = ai_game.screen
		self.screen_rect = self.ai_screen.get_rect()

		self.settings = ai_game.settings
		self.color = self.settings.bulletColor
		self.rect = pygame.Rect(0, 0, self.settings.bulletWidth, self.settings.bulletHeight)
		self.rect.midtop = ai_game.ship.rect.midtop
		
		self.y = float(self.rect.y)

	def update(self):
		"""Move the bullet upwards"""
		self.y -= self.settings.bulletSpeed
		self.rect.y = self.y
		

	def draw(self):
		pygame.draw.rect(self.ai_screen, self.color, self.rect)



