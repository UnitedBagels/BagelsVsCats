import pygame
import os
import random
import math
import operator
from bullet import *
from wheat import Wheat

pygame.init()

class Bagel(pygame.sprite.Sprite):
	bagelType = None
	health = None
	totalHealth = None
	paused = False
	bagelSelected = False

	# Bullet Physics Stuff
	fired = False
	fireTimer = 0
	shoot = None
	fireSpeed = 1

	# Blinking!
	blink = False
	holdBlink = False

	blinkTime = 0  # Changes
	blinkTimer = 0

	holdBlinkTime = 10
	holdBlinkTimer = 0

	# Why
	storedx = 0
	storedy = 0

	# Wheat Bagel Stuff
	wheatTimer = 0
	wheatTime = random.randrange(1800,2000)
	createWheat = False
	holdStretchTimer = 0
	wheatSpeed = 1

	# Hey sesame is actually not boring
	immune = False

	# Wizard!
	level = 1
	levelUp = False
	exp_list = []

	# Cow Stuff
	emptyBagel = None
	cheeseItUp = 0
	milkLeft = 10
	zzzHeight = 10
	zzzAlpha = 255
	cow_zzz = pygame.font.Font("visitor1.ttf",35).render("z",False,(0,0,0))
	sleepTimer = 800

	# Crasin Stuff
	remoteTimer = 0

	# Everything Stuff
	shotCount = 0

	# Multigrain Stuff
	fistTimer = 25
	holdMelon = False
	holdMelonTimer = 200
	blockChance = 0

	# Flagel Stuff
	exploded = False
	explosionTimer = 30
	triggered = False

	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface([66, 66])
		#self.image.set_alpha(129)
		#self.image.fill((255,255,255))  
		self.rect = pygame.Surface([66,66]).get_rect()
		self.rect.x = x
		self.rect.y = y
		self.storedx = x
		self.storedy = y
		# More Wheat Bagel Stuff
		self.wheatTime = random.randrange(600,1200)
		self.targetGroupX = {}


	def reInit(self,bagelType,image,health):
		self.bagelType = bagelType
		self.image = image
		self.health = health
		self.totalHealth = health
		self.mask = pygame.mask.from_surface(self.image)
		if bagelType == "wizard":
			self.rect.x += 8
			self.rect.y += 2
		elif bagelType == "cow":
			self.rect = self.image.get_rect()
			self.rect.x = self.storedx - 63
			self.rect.y = self.storedy
		else:
			self.rect.x += 8
			self.rect.y += 12
		self.blinkTime = random.randrange(50,350)  # Changes
		if self.bagelType == "multi":
			self.blockChance = random.choice([1,2])



	def fire(self,bulletImage,bulletList,allSprites,catList,poppy_shot,sesame_shot,garlic_shot):
		if self.cheeseItUp > 0 and self.bagelType != "multi":
			if self.paused == False:
				self.cheeseItUp -= 1
				self.fireSpeed = 4
		else:
			if self.bagelType != "multi":
				self.fireSpeed = 1
			else:
				pass

		if self.bagelType == "plain":
			for i in catList:
				if (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= 800):
					self.fired = True
					self.shoot = i

			if self.fired == True and self.paused == False:
				self.fireTimer += self.fireSpeed

			if self.shoot not in catList:
				self.fired = False

			if self.fireTimer >= 60:
				bullet = Bullet(self.rect.x + 21, self.rect.y + 13, bulletImage, "plain", 1, 0, False)
				bullet.add(bulletList)
				bullet.add(allSprites)
				bullet.bulletType = "bagel"
				self.fireTimer = 0

		elif self.bagelType == "poppy":
			for i in catList:
				if (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= 800):
					self.fired = True
					self.shoot = i

			if self.fired == True and self.paused == False:
				self.fireTimer += self.fireSpeed

			if self.shoot not in catList:
				self.fired = False

			if self.fireTimer >= 30:
				bullet = Bullet(self.rect.x + 23, self.rect.y + 15, bulletImage, "poppy", 0.5, 0, False)
				bullet.add(bulletList)
				bullet.add(allSprites)
				self.fireTimer = 0

		elif self.bagelType == "wizard":
			for i in catList:
				if (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= 800):
					self.fired = True
					self.shoot = i

			if self.fired == True and self.paused == False:
				self.fireTimer += self.fireSpeed

			if self.shoot not in catList:
				self.fired = False

			if self.fireTimer >= 200:
				if self.level == 1 or self.level == 2:
					bullet = Bullet(self.rect.x + 21, self.rect.y + 35, bulletImage, "wizard", 5, self.rect.y, False)
					bullet.add(bulletList)
					bullet.add(allSprites)
					bullet.type = "wizard"
					bullet.speed = 6
					if self.level == 1:
						bullet.level = 1
					elif self.level == 2:
						bullet.level = 2
				elif self.level == 3:
					bullet = Bullet(self.rect.x + 23, self.rect.y + 15, bulletImage, "wizard", 5, self.rect.y, False)
					bullet.add(bulletList)
					bullet.add(allSprites)
					bullet.level = 3
					bullet.speed = 8
					bullet2 = Bullet(self.rect.x + 23, self.rect.y + 15, bulletImage, "wizard", 5, self.rect.y, True)
					bullet2.add(bulletList)
					bullet2.add(allSprites)
					bullet2.level = 3
					bullet2.speed = 8
				self.fireTimer = 0

		elif self.bagelType == "everything":
			for i in catList:
				if (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= 800):
					self.fired = True
					self.shoot = i

			if self.fired == True and self.paused == False:
				self.fireTimer += self.fireSpeed

			if self.shoot not in catList:
				self.fired = False

			if self.fireTimer >= 45:
				if self.shotCount == 0:
					bullet = Bullet(self.rect.x + 23, self.rect.y + 15, poppy_shot, "poppy", 0.5, 0, False)
					bullet.add(bulletList)
					bullet.add(allSprites)
				elif self.shotCount == 1:
					bullet = Bullet(self.rect.x + 23, self.rect.y + 15, sesame_shot, "sesame", 1, 0, False)
					bullet.add(bulletList)
					bullet.add(allSprites)
				elif self.shotCount == 2:
					bullet = Bullet(self.rect.x + 23, self.rect.y + 15, garlic_shot, "garlic", 0, 0, False)
					bullet.add(bulletList)
					bullet.add(allSprites)
				self.fireTimer = 0
				
				if self.shotCount >= 2:
					self.shotCount = 0
				else:
					self.shotCount += 1

		elif self.bagelType == "multi":
			for i in catList:
				if (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= (self.rect.x + 80)):
					self.fired = True
					self.shoot = i

			if self.fired == True and self.paused == False:
				self.fireTimer += self.fireSpeed
				self.holdMelon = False
				self.holdMelonTimer = 200

			if self.shoot not in catList:
				self.fired = False
				self.fireSpeed = 1

			if self.fireTimer >= 100:
				if self.fireSpeed <= 20:
					self.fireSpeed += 1
				self.fistTimer -= 1
				if self.fistTimer == 24:
					if self.shoot.shield > 0:
						self.shoot.shield -= 4
					else:
						self.shoot.health -= 4
				if self.fistTimer <= 0:
					self.fireTimer = 0

	def animate(self,paused,bagel_blink,wheat_blink,plain_bagel,wheat_bagel,poppy_bagel,poppy_bagel_blink,poppy_bagel_shooting,poppy_bagel_shooting_blink,sesame_bagel,sesame_bagel_blink,wizard_bagel1,wizard_bagel1_blink,wizard_bagel2,wizard_bagel2_blink,wizard_bagel3,wizard_bagel3_blink,cow_bagel,cow_bagel_blink,everything_bagel,everything_bagel_blink,everything_bagel_shooting,everything_bagel_shooting_blink,crais_bagel,crais_bagel_blink,multigrain,multigrain_blink,multigrain_angry,multigrain_angry_blink,flagel,flagel_blink):
		self.paused = paused
		if self.blink == False:
			self.blinkTimer += 1
		if self.holdBlink == True:
			self.holdBlinkTimer += 1

		if self.blinkTimer >= self.blinkTime:
			self.blink = True
			self.holdBlink = True
			self.blinkTimer = 0
			self.blinkTime = random.randrange(50,350)
			if self.bagelType == "plain":
				self.image = bagel_blink
			elif self.bagelType == "wheat":
				self.image = wheat_blink
			elif self.bagelType == "poppy": # Poppy Specific
				if self.fired == True:
					self.image = poppy_bagel_shooting_blink
				else:
					self.image = poppy_bagel_blink
			elif self.bagelType == "sesame":
				self.image = sesame_bagel_blink
			elif self.bagelType == "wizard":
				if self.level == 1:
					self.image = wizard_bagel1_blink
				elif self.level == 2:
					self.image = wizard_bagel2_blink
				elif self.level == 3:
					self.image = wizard_bagel3_blink
			elif self.bagelType == "cow" and self.milkLeft > 0:
				self.image = cow_bagel_blink
			elif self.bagelType == "everything":
				if self.fired == True:
					self.image = everything_bagel_shooting_blink
				else:
					self.image = everything_bagel_blink
			elif self.bagelType == "crais":
				self.image = crais_bagel_blink
			elif self.bagelType == "multi":
				if self.fired == True:
					self.image = multigrain_angry_blink
				else:
					self.image = multigrain_blink
			elif self.bagelType == "flagel" and self.explosionTimer == 30:
				self.image = flagel_blink

		elif self.holdBlinkTimer >= self.holdBlinkTime:
			self.blink = False
			self.holdBlink = False
			self.holdBlinkTimer = 0
			if self.bagelType == "plain":
				self.image = plain_bagel
			elif self.bagelType == "wheat":
				self.image = wheat_bagel
			elif self.bagelType == "poppy":
				if self.fired == True:
					self.image = poppy_bagel_shooting
				else:
					self.image = poppy_bagel
			elif self.bagelType == "sesame":
				self.image = sesame_bagel
			elif self.bagelType == "wizard":
				if self.level == 1:
					self.image = wizard_bagel1
				elif self.level == 2:
					self.image = wizard_bagel2
				elif self.level == 3:
					self.image = wizard_bagel3
			elif self.bagelType == "cow" and self.milkLeft > 0:
				self.image = cow_bagel
			elif self.bagelType == "everything":
				if self.fired == True:
					self.image = everything_bagel_shooting
				else:
					self.image = everything_bagel
			elif self.bagelType == "crais":
				self.image = crais_bagel
			elif self.bagelType == "multi":
				if self.fired == True:
					self.image = multigrain_angry
				else:
					self.image = multigrain
			elif self.bagelType == "flagel" and self.explosionTimer == 30:
				self.image = flagel

		# Specific to certain bagels

		if self.bagelType == "poppy":
			if self.fired == True and self.blink == False:
				self.image = poppy_bagel_shooting
			elif self.fire == False:
				self.image = poppy_bagel

		if self.bagelType == "cow":
			if self.milkLeft <= 0:
				self.image = cow_bagel_blink
			if self.sleepTimer == 800:
				self.image = cow_bagel

		if self.bagelType == "everything":
			if self.fired == True and self.blink == False:
				self.image = everything_bagel_shooting
			elif self.fire == False:
				self.image = everything_bagel

		if self.bagelType == "multi":
			if self.fired == True and self.blink == False:
				self.image = multigrain_angry
			elif self.fire == False:
				self.image = multigrain

	def spawnWheat(self,wheat_stretch,wheat_bagel,wheat_image,wheatList,allSprites):
		if self.cheeseItUp > 0 :
			if self.paused == False:
				self.cheeseItUp -= 1
				self.wheatSpeed = 20
		else:
			self.wheatSpeed = 1

		if self.bagelType == "wheat":
			if self.createWheat == False and self.paused == False:
				self.wheatTimer += self.wheatSpeed
			if self.wheatTimer >= self.wheatTime and self.paused == False:
				self.createWheat = True
				self.wheatTimer = 0

		if self.createWheat == True and self.paused == False:
			self.image = wheat_stretch
			self.holdStretchTimer += 1
			if self.holdStretchTimer >= 60:
				self.image = wheat_bagel
				self.createWheat = False
				self.holdStretchTimer = 0
				wheat = Wheat(self.rect.x,self.rect.y - 40,wheat_image)
				wheat.add(wheatList)
				wheat.add(allSprites)
				self.wheatTime = random.randrange(1800,2000)

	def destroy(self,bagelList,emptyBList,emptyCowBList):
		if self.bagelType != None and self.health <= 0:
			if self.bagelType == "backSprite":
				for i in bagelList:
					if i.cowNumber == self.cowNumber:
						i.health = 0
			self.remove(bagelList)
			self.add(emptyBList)
			self.image = None
			self.rect = pygame.Surface([66,66]).get_rect()
			self.rect.x = self.storedx
			self.rect.y = self.storedy
			self.health = 0
			self.level = 1
			self.fireTimer = 0
			self.wheatTime = random.randrange(1800,2000)
			self.wheatTimer = 0
			self.wheatSpeed = 1
			self.holdStretchTimer = 0
			self.createWheat = False
			self.shoot = None
			self.remoteTimer = 0
			self.fistTimer = 0
			self.holdMelon = False
			self.holdMelonTimer = 200
			self.blockChance = 0
			self.fireSpeed = 1
			self.targetGroupX = {}
			self.explosionTimer = 30
			self.triggered = False
			if self.bagelType == "cow":
				self.emptyBagel.remove(emptyCowBList)
				self.emptyBagel.kill()
				self.emptyBagel = None
			self.bagelType = None

		# The no where else to put stuff section #Fantastic
		if self.milkLeft <= 0 and self.bagelType == "cow":
			self.sleepTimer -= 1
			if self.sleepTimer <= 0:
				self.milkLeft = 10
				self.sleepTimer = 800

		if self.bagelType == "sesame":
			if self.cheeseItUp > 0:
				self.immune = True
			else:
				self.immune = False

	def dropIt(self,cage,catList,allSprites,cageList):
		if self.cheeseItUp > 0:
			if self.paused == False:
				self.cheeseItUp -= 1
		else:
			self.fireSpeed = 1

		for i in catList:
			if (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= 800) and i.targeted == False and i.catType != "baby_cat":
				if i not in self.targetGroupX.values():
					self.targetGroupX[i.catNumber] = i

			if i in self.targetGroupX.values() and self.shoot == None and (i.rect.y <= self.rect.y <= i.rect.y + 21 or i.rect.y <= self.rect.y + 21 <= i.rect.y + 21) and (i.rect.x > self.rect.x) and (i.rect.x <= 800) and i.targeted == False:
				minimum = min(self.targetGroupX, key=self.targetGroupX.get)
				self.shoot = self.targetGroupX[minimum]
				self.shoot.targeted = True
				self.fired = True

		#print(self.targetGroupX)
		if self.fired == True and self.paused == False:
			self.fireTimer += self.fireSpeed

		if self.shoot not in catList and self.fired == True:
			self.fired = False
			if self.shoot != None:
				del self.targetGroupX[self.shoot.catNumber]
			self.shoot = None

		if self.fireTimer >= 375:
			if self.shoot != None:
				if self.shoot.victim != None:
					catCage = Cage(self.shoot.rect.x - 15, -400, cage, self.shoot.storedY - 6)
					catCage.add(cageList)
					catCage.add(allSprites)
					if self.cheeseItUp > 0:
						catCage.dogInside = True
				else:
					catCage = Cage(self.shoot.rect.x - 100, -400, cage, self.shoot.storedY - 6)
					catCage.add(cageList)
					catCage.add(allSprites)
					if self.cheeseItUp > 0:
						catCage.dogInside = True
				self.fireTimer = 0

	def erosion(self,catList,allSprites,explosionList,flagel_puff1,flagel_puff2,extinction):
		if pygame.sprite.spritecollide(self, catList, False, pygame.sprite.collide_mask):
			self.triggered = True

		if self.triggered == True:
			if self.explosionTimer == 30:
				self.rect.x -= 5
				self.rect.y -= 5
			if 10 < self.explosionTimer <= 30:
				self.image = flagel_puff1
			elif 0 < self.explosionTimer <= 10:
				self.image = flagel_puff2
			elif self.explosionTimer <= 0:
				if self.cheeseItUp == False:
					explosion = Explosion(self.storedx,self.storedy)
					explosion.add(allSprites)
					explosion.add(explosionList)
				else:
					extinction[0] = 255
					for i in catList:
						i.kill()
						i.remove()
				self.health = 0
			self.explosionTimer -= 1
			#print("woowowoowooo")

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)

class GhostBagel(pygame.sprite.Sprite):

	degrees = 0
	rotationTimer = 0

	def __init__(self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x_velocity = random.randrange(-5, -1)
		self.y_velocity = random.randrange(1, 5)
		self.gravity = 0.1

	def update(self):
		self.y_velocity += self.gravity
		self.rect.x += self.x_velocity
		self.rect.y += self.y_velocity

		if self.rect.x <= -50 or self.rect.x >= 800 or self.rect.y <= 0 or self.rect.y >= 522:
			self.kill()
			self.remove()

	def rot_center(self):
		orig_rect = self.image.get_rect()
		rot_image = pygame.transform.rotate(self.image, 180)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		self.image = rot_image.subsurface(rot_rect).copy()

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)

class emptyBagel(pygame.sprite.Sprite):

	def __init__(self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)
		

class creamCheese(pygame.sprite.Sprite):
	def __init__(self,x,y,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def __getstate__(self):
	    d = dict(self.__dict__)
	    if 'image' in d: del d['image']
	    if 'mask' in d: del d['mask']
	    return d

	def __setstate__(self, d):
		self.__dict__.update(d)









		
		
