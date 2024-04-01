import pygame
import sys
from settings import Settings
from ship import Ship
from bullets import Bullets
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
	"""Major class to control the whole game"""
	def __init__(self):
		"""Initialise the game"""
		pygame.init()
		self.settings = Settings()
		
		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screenWidth = self.screen.get_rect().width
		self.settings.screenHeight = self.screen.get_rect().height

		pygame.display.set_caption("Alien Invasion")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		self.bg_color = self.settings.bgColor

		#Play button
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Run the game in loop"""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.updateLoc()
				self._update_bullet()
				self._update_aliens()
			self._update_events()
			

	def _update_events(self):
		#Filling the background color
		self.screen.fill(self.bg_color)

		#Drawing the ship on screen
		self.ship.blitme()

		#Redraw the screen with the desired background
		for bullet in self.bullets.sprites():
			bullet.draw()
		
		#Draw aliens
		self.aliens.draw(self.screen)

		#Draw score info
		self.sb.show_score()

		#Draw play button if the game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()

	def _check_events(self):
		"""Check the events and generate response"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
	
	def _check_play_button(self, mouse_pos):
		"""Start a new game when player clicks play button"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#Reset the game settings
			self.settings.initialize_dynamic_settings()

			#Reset game statistics
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Remove remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Crete a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#Hide the mouse cursor
			pygame.mouse.set_visible(False)

	
	def _check_keydown_events(self, event):
		"""Checks and responds for Key DOWN events"""
		if event.key == pygame.K_RIGHT:
			self.ship.movingRight = True
		elif event.key == pygame.K_LEFT:
			self.ship.movingLeft = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""Checks and responds for Key UP events"""
		if event.key == pygame.K_RIGHT:
			self.ship.movingRight = False
		if event.key == pygame.K_LEFT:
			self.ship.movingLeft = False

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bulletsAllowed:
			new_bullet = Bullets(self)
			self.bullets.add(new_bullet)

	def _update_bullet(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0 :
				self.bullets.remove(bullet)

		self._check_bullets_alien_collisions()
	
	def _check_bullets_alien_collisions(self):
		"""Responds to bullet and alien collision"""
		##Check if bullets collide and remove them
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#Remove existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""Updates the position of all the aliens."""
		self._check_fleet_edges()
		self.aliens.update()

		#Check alien ship collison
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		
		#Check for aliens hitting bottom of the screen
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Respond to the ship being hit bu an alien"""
		if self.stats.ships_left > 0:
			#Decrement ships left
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#Pause
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	
	def _check_aliens_bottom(self):
		"""Check if any alien reached the bottom"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if the ship got hit.
				self._ship_hit()
				break

	
	def _create_fleet(self):
		"""Create Aliens and add to the group"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space = self.settings.screen_width - (2 * alien_width)
		number_of_aliens_x = available_space // (2 * alien_width)
		number_rows = self.settings.screen_height  // (3 * alien_height)

		#Create the full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_of_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 3 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien_height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Responds when aliens reach the edges"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	
	def _change_fleet_direction(self):
		"""Drop the entire fleet and changes the direction"""
		flag = 0
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
			if flag == 0:
				self.settings.fleet_direction *= -1
				flag += 1

if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()