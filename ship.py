import pygame
from settings import Settings
from pygame.sprite import Sprite

class Ship(Sprite):
	"""To store the belongings of ship"""
	def __init__(self,ai_game):
		"""Initialise the ship and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		self.shipSetting = Settings()

		#Load the ship image and get its rect
		self.image = pygame.image.load("images/ship.bmp")
		self.rect = self.image.get_rect()

		#Start each ship at the center of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		self.rect.width = 40
		self.rect.height = 100

		self.movingRight = False
		self.movingLeft = False

		self.x = float(self.rect.x)

	def updateLoc(self):
		if self.movingRight and self.rect.right < self.screen_rect.right:
			self.x += self.shipSetting.ship_speed

		elif self.movingLeft and self.x > 0:
			self.x -= self.shipSetting.ship_speed

		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship in its current postion"""
		self.screen.blit(self.image, self.rect)
	
	def center_ship(self):
		"""Center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)