class Settings:
	""" A class to store the setting variables for Alien Invasion"""
	def __init__(self):
		"""Initialising the static settings for the game"""
		#Screen Settings
		self.screen_width = 1000
		self.screen_height = 600
		self.bgColor = (255, 220, 240)

		#ship settings
		self.ship_limit = 3

		#Bullet settings
		self.bulletWidth = 30
		self.bulletHeight = 15
		self.bulletColor = (60, 60, 60)
		self.bulletsAllowed = 3

		#Alien Settings
		self.fleet_drop_speed = 100

		#How quickly game speeds up
		self.speedup_scale = 1.1
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed = 1.5
		self.bulletSpeed = 2 
		self.alien_speed = 0.1

		#fleet direction
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 10
	
	def increase_speed(self):
		"""Increase speed settings and point values"""
		self.ship_speed *=  self.speedup_scale
		self.bulletSpeed *= self.speedup_scale 
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)




