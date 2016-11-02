import pygame
import random

pygame.init()

class Wheat(pygame.sprite.Sprite):
	
	paused = False
	move = True

	def __init__(self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed = -6

	def update(self, paused):
		if paused == False:
			if self.rect.y < 348 and self.move == True:
				self.rect.y += self.speed
			if self.rect.y <= -200:
				self.speed = 1
				self.rect.x = random.randrange(0,750)
		if self.rect.x > 750:
			self.rect.x = 750

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)

		
