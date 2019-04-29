import pygame
import random

class Particle(pygame.sprite.Sprite):

	paused = False
	time = 0
	stop_y = 0
	stop_x_l = 0
	stop_x_r = 0
	display_time = 0
	passed = False

	def __init__(self, x, y, dx, dy, size, color, height, p_type):
		pygame.sprite.Sprite.__init__(self)
		self.p_type = p_type
		if self.p_type == "exp":
			size = random.randint(3, 6)
		self.image = pygame.Surface((size, size))
		self.image.fill(color)
		self.rect = self.image.get_rect()

		self.x_velocity = dx
		self.y_velocity = dy
		self.rect.x = x
		self.rect.y = y
		self.p_type = p_type
		self.stop_y = self.rect.y + height
		self.gravity = 0.35

	def update(self, paused):
		self.paused = paused
		if self.paused == False:
			self.y_velocity += self.gravity
			self.time += 1

			if self.p_type != "high":
				if self.rect.y <= self.stop_y:
					self.rect.x += self.x_velocity
					self.rect.y += self.y_velocity
			else:
				if self.rect.y < self.stop_y:
					self.passed = True
				if self.rect.y >= self.stop_y and self.passed == False:
					self.rect.x += self.x_velocity
					self.rect.y += self.y_velocity
				elif self.rect.y <= self.stop_y and self.passed == True:
					self.rect.x += self.x_velocity
					self.rect.y += self.y_velocity

		"""if self.p_type == "high":
			if self.rect.y_velocity < 0:
				self.passed = True"""
 
	def display(self, main_surface):
		if self.time <= 100:
			main_surface.blit(self.image, (self.rect.x, self.rect.y))

	def killEverything(self,p_list):
		particle_list = p_list

		lifetime = 100
		if self.p_type == "quick":
			lifetime = 5

		if self.time >= lifetime or (self.rect.y >= self.stop_y and self.p_type == "exp") or (self.rect.y >= 400):
			self.kill()
			particle_list.remove(self)
			#tuby the tuba

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)