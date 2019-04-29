import pygame
import random
import math
from dog import Dog
from math import sin
from wheat import CDOrb


pygame.init()

class Bullet(pygame.sprite.Sprite):

	moving = True
	speed = None
	hitList = None
	step = 1
	level = 0

	# Mini Bagels
	bulletHeight = 0

	def __init__(self, x, y, image, bulletType, damage, bagely, inverse):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.bulletType = bulletType
		if self.bulletType != "wizard":
			if self.bulletType == "first_plain":
				self.speed = 12
			else:
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

class Trail(pygame.sprite.Sprite):

	trailCat = None
	countdown = 1000

	def __init__(self, x, y, catNumber, cat):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([900,36])
		self.image.fill((255,201,41))
		self.rect = self.image.get_rect()
		self.rect.x = x + 12
		self.rect.y = y + 6
		self.trailNumber = catNumber
		self.trailCat = cat

	def update(self):
		#print(self.rect.x,self.trailCat.rect.x)
		if self.rect.x >= self.trailCat.rect.x + 12:
			self.rect.x = self.trailCat.rect.x + 12

		if self.trailCat.health <= 0:
			self.countdown -= 1
			if self.countdown <= 1:
				self.kill()
				self.remove()

class Cannon(pygame.sprite.Sprite):

	damage = 20
	startY = 0

	def __init__(self, x, y, dx, dy, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()

		self.x_velocity = dx
		self.y_velocity = dy
		self.rect.x = x
		self.rect.y = y
		self.startY = y

	def update(self,paused):
		if not paused:
			self.y_velocity += 0.35 # Gravity
			self.rect.x += self.x_velocity
			self.rect.y += self.y_velocity

			if self.rect.y >= 580:
				self.kill()
				self.remove()

class AlienBullet(pygame.sprite.Sprite):

	dy = 0
	target = None

	def __init__(self, x, y, image,target):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.dy = -7
		self.target = target

	def update(self,paused,wheatList,allSprites,cd_orb):
		if not paused:
			self.rect.y += self.dy

			if self.rect.y < -500:
				self.dy = 15
				self.rect.x = self.target.rect.x + 20

			if self.rect.y >= self.target.rect.y - 25 and self.target.bagelType != None and self.dy == 15:
				self.target.health = 0
				orb = CDOrb(self.target.storedx + 11,self.target.storedy + 11,cd_orb)
				orb.add(allSprites)
				orb.add(wheatList)
				self.kill()
				self.remove()

			if self.rect.y >= 580: # Just in case it passes the edge of the screen
				self.kill()
				self.remove()



