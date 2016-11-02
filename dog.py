import pygame

class Dog(pygame.sprite.Sprite):

	health = 360
	totalHealth = 360
	victim = None
	eatAnimationTime = 0
	move = True
	eat = False
	immune = False # The laziest way to solve any problem ever
	bagelType = "dog" # And this too

	def __init__(self,x,y,image,image_eating):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.image_eating = image_eating
		self.dog = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self,paused):
		# This is literally copied and pasted from the cat's eat function
		if self.move == True:
			self.rect.x += 1
		if self.rect.x > 875 or self.health <= 0: # He was invincible ... was ...
			self.kill()
			self.remove()

		if self.eat == True: # Except for this line
			if 10 <= self.eatAnimationTime <= 30:
				self.image = self.image_eating
			elif self.eatAnimationTime <= 10:
				self.image = self.dog
			elif self.eatAnimationTime >= 30:
				self.eatAnimationTime = 0
				self.image = self.image_eating
			if self.eatAnimationTime == 20:
				if self.victim.shield > 0:
					self.victim.shield -= 6
				else:
					self.victim.health -= 6

		if self.victim != None:
			self.eat = True
			self.move = False
			self.victim.move = False
			if self.victim.health <= 0:
				self.victim = None
				self.eat = False
				self.move = True

		if self.eat == True and paused == False:
			self.eatAnimationTime += 1

		elif self.eat == False:
			self.eatAnimationTime = 0
			self.image = self.dog
