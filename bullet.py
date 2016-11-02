import pygame
import random
import math
from dog import Dog
from math import sin


pygame.init()

class Bullet(pygame.sprite.Sprite):

	moving = True
	speed = None
	hitList = None
	step = 1
	level = 0

	def __init__(self, x, y, image, bulletType, damage, bagely, inverse):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.bulletType = bulletType
		if self.bulletType != "wizard":
			self.speed = random.randrange(5,7)
		self.bagely = bagely

		self.inverse = inverse
		self.damage = damage
		self.hitList = pygame.sprite.Group()

	def update(self, paused):
		self.paused = paused
		if self.paused == False:
			self.step += 0.02
			if self.bulletType == "wizard" and self.level == 3:
				if self.inverse == False:
					self.rect.y = (math.sin(self.step * 15) * 10 + self.bagely) + 35 # 15
				elif self.inverse == True:
					self.rect.y = (-math.sin(self.step * 15) * 10 + self.bagely) + 35 # 15

			self.rect.x += self.speed
			if self.rect.x >= 900:
				self.kill()
				self.remove()

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)

class Cage(pygame.sprite.Sprite):

	stopped = False
	stopPoint = 0
	victim = None
	disTimer = 0
	hitList = None
	dogInside = False

	def __init__(self, x, y, image, stopPoint):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.stopPoint = stopPoint
		self.hitList = pygame.sprite.Group()

	def update(self,paused,big_cage,dogImg,dogImgEating,dogList):
		self.paused = paused
		if self.rect.y < self.stopPoint and self.paused == False:
			self.rect.y += 7
		elif self.rect.y >= self.stopPoint and self.paused == False:
			self.rect.y = self.stopPoint
			self.stopped = True

		if self.victim != None and self.victim.catType == "weenie_cat":
			self.image = big_cage

		if self.stopped:
			if self.dogInside == True:
				bigDog = Dog(self.rect.x + 10,self.rect.y + 8,dogImg,dogImgEating)
				bigDog.add(dogList)
				self.dogInside = False
			self.disTimer += 1
			if self.disTimer >= 350:
				self.disTimer = 0
				self.kill()
				if self.victim != None:
					self.victim.move = True
					self.victim.caged = False

		if self.rect.y > 480: #probably not
			self.kill()

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)

class Explosion(pygame.sprite.Sprite):
	extinction = 0

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([198,198])
		self.rect = self.image.get_rect()
		self.rect.x = x - 72
		self.rect.y = y - 75
		self.formParticles = True

	def update(self):
		self.kill()
		self.remove()
		pass
		#print("weegle")