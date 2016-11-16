import pygame, os
from bagel import GhostBagel
from bullet import Bullet
from wheat import Wheat

pygame.init()

class Cat(pygame.sprite.Sprite):
	paused = False
	cat = None
	move = True
	gameOver = False
	catNumber = None
	storedSpeed = 1

	# Eating
	eat = False
	victim = None
	eatAnimationTime = 0

	# Melon Stuff
	fired = False
	fireTimer = 0
	shoot = None
	afterShot = 0

	# Weenies!
	sp1 = False
	sp2 = False
	sp3 = False
	sp4 = False
	sp5 = False
	speed = 1

	# Pizza .. cat?
	shield = None
	totalShield = None
	pizzaDown = False

	# Cage Stuff
	caged = False
	storedY = 0
	targeted = False

	# Everything Stuff
	garlicStacks = 0
	garlicTimer = 0
	healthTick = 0

	def __init__(self,catType,health,x,y,image,image_eating,number):
		pygame.sprite.Sprite.__init__(self)
		self.health = health
		self.totalHealth = health
		self.image = image
		self.cat = image
		self.image_eating = image_eating
		self.catType = catType
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.catNumber = number
		# dont put in init!
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, paused):
		self.paused = paused
		if self.paused == False:
			if self.move == True:
				self.rect.x -= self.speed
			if self.rect.x <= -100:
				self.kill()
				self.remove()
			if self.rect.x < 0:
				self.gameOver = True

			if self.garlicStacks != 0:
				self.garlicTimer += 1
				if self.garlicTimer >= 60: #150
					self.healthTick += 1
					if self.healthTick == 20:
						if self.shield > 0:
							self.shield -= 1
						else:
							self.health -= 1
					elif self.healthTick == 40:
						if self.shield > 0:
							self.shield -= 1
						else:
							self.health -= 1
						self.garlicTimer = 0
						self.healthTick = 0

		# It's rainin' pizzas
	def rainPizzas(self,pizza,allSprites,ghostBagelList,pizza_cat_ns,pizza_cat_eating_ns): #ns = no shield
		if self.shield <= 0:
			if self.pizzaDown == False:
				self.cat = pizza_cat_ns
				self.image_eating = pizza_cat_eating_ns
				flyingPizza = GhostBagel(self.rect.x,self.rect.y,pizza)
				flyingPizza.add(allSprites)
				flyingPizza.add(ghostBagelList)
				px = self.rect.x
				py = self.rect.y
				self.rect = self.image.get_rect()
				self.rect.x = px
				self.rect.y = py
				if self.eat == False:
					self.rect.x += 11
				self.pizzaDown = True

	def eatEmCat(self,bagelList,emptyBList):
		if 10 <= self.eatAnimationTime <= 30:
			self.image = self.image_eating
		elif self.eatAnimationTime <= 10:
			self.image = self.cat
		elif self.eatAnimationTime >= 30:
			self.eatAnimationTime = 0
			self.image = self.image_eating

		if self.victim != None and self.caged == False:
			self.eat = True
			self.move = False
			if self.victim.health <= 0 and self.victim.immune == False:
				self.victim = None
				self.eat = False
				self.move = True

		if self.eat == True and self.paused == False:
			if self.victim.immune == False:
				if self.catType != "ninja_cat":
					self.victim.health -= 1
				else:
					self.victim.health -= 2
			self.eatAnimationTime += 1
			self.fired = False
			self.fireTimer = 0
			self.shoot = None
			self.afterShot = 0

		elif self.eat == False:
			self.eatAnimationTime = 0


	def eatEmTacoCat(self,bagelList,emptyBList,ghostBagelList,allSprites,plain,poppy,wizard_bagel1,wizard_bagel2,wizard_bagel3,every,crais):
		if self.victim != None and self.caged == False:
			self.eat = True
			self.move = False

		if 10 <= self.eatAnimationTime <= 30:
			self.image = self.image_eating
		elif self.eatAnimationTime <= 10:
			self.image = self.cat
		elif self.eatAnimationTime >= 30:
			self.eatAnimationTime = 0
			self.image = self.image_eating

		if self.eat == True and self.paused == False and self.caged == False:
			if self.victim.bagelType == "wheat" or self.victim.bagelType == "sesame" or self.victim.bagelType == "cow" or self.victim.bagelType == "multi":	
				self.eatAnimationTime += 1
				if self.victim.immune == False:
					self.victim.health -= 1

			elif self.victim.bagelType == "plain" or self.victim.bagelType == "poppy" or self.victim.bagelType == "wizard" or self.victim.bagelType == "everything" or self.victim.bagelType == "crais":
				if self.victim.bagelType == "plain":
					ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,plain)
					ghostBagel.add(allSprites)
					ghostBagel.add(ghostBagelList)
				elif self.victim.bagelType == "poppy":
					ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,poppy)
					ghostBagel.add(allSprites)
					ghostBagel.add(ghostBagelList)
				elif self.victim.bagelType == "wizard":
					if self.victim.level == 1:
						ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,wizard_bagel1)
						ghostBagel.add(allSprites)
						ghostBagel.add(ghostBagelList)
					elif self.victim.level == 2:
						ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,wizard_bagel2)
						ghostBagel.add(allSprites)
						ghostBagel.add(ghostBagelList)
					elif self.victim.level == 3:
						ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,wizard_bagel3)
						ghostBagel.add(allSprites)
						ghostBagel.add(ghostBagelList)
				elif self.victim.bagelType == "everything":
					ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,every)
					ghostBagel.add(allSprites)
					ghostBagel.add(ghostBagelList)
				elif self.victim.bagelType == "crais":
					ghostBagel = GhostBagel(self.victim.rect.x,self.victim.rect.y,crais)
					ghostBagel.add(allSprites)
					ghostBagel.add(ghostBagelList)

				self.move = True
				self.victim.remove(bagelList)
				self.victim.add(emptyBList)
				self.victim.image = None
				self.victim.rect = pygame.Surface([66,66]).get_rect()
				self.victim.rect.x = self.victim.storedx
				self.victim.rect.y = self.victim.storedy
				self.victim.bagelType = None
				self.victim.health = 0
				self.victim.level = 1
				self.victim.fireTimer = 0
				self.eat = False
				self.victim = None

			if self.victim != None and self.caged == False:
				if self.victim.health <= 0 and (self.victim.bagelType != "plain" or self.victim.bagelType != "poppy" or self.victim.bagelType != "everything" or self.victim.bagelType != "crais"): # And these two
					self.victim = None
					self.eat = False
					self.move = True

		elif self.eat == False:
			self.eatAnimationTime = 0

	def melonFire(self,bagelList,bulletImage,catBulletList,allSprites):
		for i in bagelList:
			if (i.rect.y <= self.rect.y <= i.rect.y + 23 or i.rect.y <= self.rect.y + 23 <= i.rect.y + 23) and (i.rect.x < self.rect.x) and (i.rect.x + self.rect.x >= 0) and self.eat == False and i.bagelType != "flagel": # Ignore throwing melons at flagels
				self.fired = True
				self.shoot = i

		if self.fired == True and self.eat == False and self.afterShot == 0 and self.paused == False:
			self.fireTimer += 1

		if self.shoot not in bagelList:
			self.fired = False

		if self.fireTimer >= 200:
			bullet = Bullet(self.rect.x - 12, self.rect.y + 12, bulletImage, "melon", 1, 0, False)
			bullet.add(catBulletList)
			bullet.add(allSprites)
			bullet.bulletCatType = "melon"
			bullet.speed = -6
			self.fireTimer = 0
			self.afterShot = 1

		if self.afterShot >= 1:
			self.afterShot += 1
			if self.afterShot >= 50:
				self.afterShot = 0

	def spawnBabies(self,baby_cat,baby_cat_eating,allSprites,catList):
		if self.health <= 24 and self.sp1 == False:
			self.sp1 = True
			cat = Cat("baby_cat",2,self.rect.x,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat.add(allSprites)
			cat.add(catList)
			cat.speed = 3
		if self.health <= 18 and self.sp2 == False:
			self.sp2 = True
			cat = Cat("baby_cat",2,self.rect.x,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat.add(allSprites)
			cat.add(catList)
			cat.speed = 3
		if self.health <= 12 and self.sp3 == False:
			self.sp3 = True
			cat = Cat("baby_cat",2,self.rect.x,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat.add(allSprites)
			cat.add(catList)
			cat.speed = 3
		if self.health <= 6 and self.sp4 == False:
			self.sp4 = True
			cat = Cat("baby_cat",2,self.rect.x,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat.add(allSprites)
			cat.add(catList)
			cat.speed = 3
		if self.health <= 0 and self.sp5 == False:
			self.sp5 = True
			cat = Cat("baby_cat",2,self.rect.x,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat.add(allSprites)
			cat.add(catList)
			cat.speed = 3
			cat2 = Cat("baby_cat",2,self.rect.x + 35,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat2.add(allSprites)
			cat2.add(catList)
			cat2.speed = 3
			cat3 = Cat("baby_cat",2,self.rect.x + 70,self.rect.y + 13,baby_cat,baby_cat_eating,100000000000)
			cat3.add(allSprites)
			cat3.add(catList)
			cat3.speed = 3

	def onDeath(self,wheat_image,wheatList,allSprites):
		if self.health <= 0:
			self.kill()
			self.remove()
			if self.catType != "baby_cat":
				wheat = Wheat(self.rect.x,self.storedY,wheat_image)
				wheat.move = False
				wheat.add(wheatList)
				wheat.add(allSprites)

	def draw(self, screen): # Absolutely 100% completely necessary
		screen.blit(self.image, self.rect)

	def __getstate__(self):
		d = dict(self.__dict__)
		if 'image' in d: del d['image']
		if 'mask' in d: del d['mask']
		if 'cat' in d: del d['cat']
		if 'victim' in d: del d['victim']
		if 'image_eating' in d: del d['image_eating']
		return d

	def __setstate__(self, d):
		self.__dict__.update(d)









