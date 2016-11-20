from __future__ import division

import pygame
import os
import sys
import random
import math
import pickle
import webbrowser
from math import cos
from pygame.locals import *
from bagel import Bagel
from bagel import emptyBagel
from cat import Cat
from bullet import Bullet
from bullet import Trail
from particle import Particle

try:
	import pygame.mixer as mixer
except ImportError:
	import android.mixer as mixer

try:
	import android
except ImportError:
	android = None
	
if android:
	android.init()

mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode((800,480))
title_font = pygame.font.Font("visitor1.ttf",40)
particle_list = []
paused = False

tile_map = [0]
class Game(object):

	# Title Screen
	titleOn = True
	title_screen = pygame.image.load(os.path.join("images", "title_screen.png")).convert_alpha()
	pressed_play_button = pygame.image.load(os.path.join("images", "pressed_play_button.png")).convert_alpha()
	version_font = pygame.font.Font("visitor1.ttf",30)
	version = version_font.render("Alpha 1.5.3",False,(0,0,0))
	gameOver = False

	# Pause
	pause_menu = pygame.image.load(os.path.join("images", "pause_menu.png")).convert_alpha()
	options_menu = pygame.image.load(os.path.join("images", "options_menu.png")).convert_alpha()
	info_screen = pygame.image.load(os.path.join("images", "info_screen.png")).convert_alpha()
	music_slider = pygame.image.load(os.path.join("images", "slider.png")).convert_alpha()
	sound_slider = pygame.image.load(os.path.join("images", "slider.png")).convert_alpha()
	grayed_out_music =  pygame.image.load(os.path.join("images", "grayed_out_music.png")).convert_alpha()
	grayed_out_sound =  pygame.image.load(os.path.join("images", "grayed_out_sound.png")).convert_alpha()
	grayed_out_particles_button =  pygame.image.load(os.path.join("images", "grayed_out_particles_button.png")).convert_alpha()
	game_over_screen = pygame.image.load(os.path.join("images", "game_over_screen.png")).convert_alpha()

	# Title Vars
	firstPress = False
	# Welcome!

	firstOpen = True

	# Le musiche
	bagelPlace = mixer.Sound("placing.ogg")
	bagelSplat = mixer.Sound("bagelsplat.ogg")
	poppySplat = mixer.Sound("poppysplat.ogg")
	wizardSplat = mixer.Sound("wizardsplat.ogg")
	cageDrop = mixer.Sound("cagedrop.ogg")
	punch = mixer.Sound("punch.ogg")
	fork = mixer.Sound("fork.ogg")
	soundList = [bagelPlace,bagelSplat,poppySplat,wizardSplat,cageDrop,punch,fork]

	mixer.music.load("title.ogg")
	titleRun = True
	firstRun = True


	# drawBackground
	grass = pygame.image.load(os.path.join("images", "oldgrass.png")).convert_alpha()
	plain_backing = pygame.image.load(os.path.join("images", "plain_backing.png")).convert_alpha()
	wheat_backing = pygame.image.load(os.path.join("images", "wheat_backing.png")).convert_alpha()
	poppy_backing = pygame.image.load(os.path.join("images", "poppy_backing.png")).convert_alpha()
	sesame_backing = pygame.image.load(os.path.join("images", "sesame_backing.png")).convert_alpha()
	wizard_backing = pygame.image.load(os.path.join("images", "wizard_backing.png")).convert_alpha()
	cow_backing = pygame.image.load(os.path.join("images", "cow_backing.png")).convert_alpha()
	every_backing = pygame.image.load(os.path.join("images", "everything_backing.png")).convert_alpha()
	crais_backing = pygame.image.load(os.path.join("images", "crais_backing.png")).convert_alpha()
	multi_backing = pygame.image.load(os.path.join("images", "multi_backing.png")).convert_alpha()
	flagel_backing = pygame.image.load(os.path.join("images", "flagel_backing.png")).convert_alpha()
	mini_backing = pygame.image.load(os.path.join("images", "mini_backing.png")).convert_alpha()
	numbered_sel = pygame.image.load(os.path.join("images", "numbered_sel.png")).convert_alpha()
	locked = pygame.image.load(os.path.join("images", "locked.png")).convert_alpha()
	wheat = pygame.image.load(os.path.join("images", "wheat.png")).convert_alpha()
	tile = pygame.image.load(os.path.join("images", "tile.png")).convert_alpha()
	selector = pygame.image.load(os.path.join("images", "selector.png")).convert_alpha()
	blank_tile = pygame.image.load(os.path.join("images", "blank_tile.png")).convert_alpha()
	blank_tile_dirt = pygame.image.load(os.path.join("images", "blank_tile_dirt.png")).convert_alpha()
	cream_cheese_tile = pygame.image.load(os.path.join("images", "cream_cheese_tile.png")).convert_alpha()
	selected = pygame.image.load(os.path.join("images", "selected.png")).convert_alpha()
	fork_overlay = pygame.image.load(os.path.join("images", "fork_overlay.png")).convert_alpha()
	cream_cheese_selected = pygame.image.load(os.path.join("images", "cream_cheese_selected.png")).convert_alpha()
	cream_cheese = pygame.image.load(os.path.join("images", "cream_cheese.png")).convert_alpha()
	arrows = pygame.image.load(os.path.join("images", "arrows.png")).convert_alpha()
	wheat_shine = pygame.image.load(os.path.join("images", "wheat_shine.png")).convert_alpha()
	milk_ready = pygame.image.load(os.path.join("images", "milk_ready.png")).convert_alpha()
	grassX = 0
	grassY = 0
	displayWave = 200

	# Rectangles
	box1 = pygame.Rect(220,410,100,50)
	box2 = pygame.Rect(325,410,100,50)
	box3 = pygame.Rect(430,410,100,50)
	box4 = pygame.Rect(535,410,100,50)
	box5 = pygame.Rect(640,410,100,50)
	forkBox = pygame.Rect(70,400,70,70)
	play_button = pygame.Rect(281,178,248,64)
	arrow_button = pygame.Rect(748,412,40,46)
	wheatmilk_box = pygame.Rect(145,405,70,70)
	lightBox = 0

	try:
		with open('save.dat', 'rb') as fp:
			music_slider_value = pickle.load(fp)
			sound_slider_value = pickle.load(fp)
			musicOff = pickle.load(fp)
			soundOff = pickle.load(fp)
			particleSetting = pickle.load(fp)
			fp.close()
	except EOFError:
		music_slider_value = 184
		sound_slider_value = 184
		musicOff = False
		soundOff = False
		particleSetting = False
		with open('save.dat', 'wb') as fp:
			pickle.dump(music_slider_value,fp)
			pickle.dump(sound_slider_value,fp)
			pickle.dump(musicOff,fp)
			pickle.dump(soundOff,fp)
			fp.close()

	# Paused!
	menu_button = pygame.Rect(0,400,66,66)
	resume_button = pygame.Rect(276,86,248,64)
	quit_button = pygame.Rect(276,183,248,64)
	restart_button = pygame.Rect(266,258,75,75)
	options_button = pygame.Rect(460,258,75,75)
	options_button_menu = pygame.Rect(367,353,75,75)
	info_button = pygame.Rect(280,272,248,64)
	info_back = pygame.Rect(268,281,89,48)
	wiki_info = pygame.Rect(374,271,122,44)
	options_back = pygame.Rect(273,92,76,38)
	music_button = pygame.Rect(361,74,75,75)
	sound_button = pygame.Rect(450,74,75,75)
	particles_button = pygame.Rect(493,271,38,38)
	music_slider_button = pygame.Rect(296,180,191,7)
	sound_slider_button = pygame.Rect(296,225,191,7)
	options = False
	info = False
	restart = False
	game_over_restart_button = pygame.Rect(362,209,75,75)

	# mousePos
	clicked = False

	# Drawings
	plain_bagel = pygame.image.load(os.path.join("images", "bagel.png")).convert_alpha()
	wheat_bagel = pygame.image.load(os.path.join("images", "wheat_bagel.png")).convert_alpha()
	bagel_blink = pygame.image.load(os.path.join("images", "bagel_blink.png")).convert_alpha()
	wheat_blink = pygame.image.load(os.path.join("images", "wheat_blink.png")).convert_alpha()
	wheat_stretch = pygame.image.load(os.path.join("images", "wheat_stretch.png")).convert_alpha()
	poppy_bagel = pygame.image.load(os.path.join("images", "poppy_bagel.png")).convert_alpha()
	poppy_bagel_blink = pygame.image.load(os.path.join("images", "poppy_bagel_blink.png")).convert_alpha()
	poppy_bagel_shooting = pygame.image.load(os.path.join("images", "poppy_bagel_shooting.png")).convert_alpha()
	poppy_bagel_shooting_blink = pygame.image.load(os.path.join("images", "poppy_bagel_shooting_blink.png")).convert_alpha()
	sesame_bagel = pygame.image.load(os.path.join("images", "sesame_bagel.png")).convert_alpha()
	sesame_bagel_blink = pygame.image.load(os.path.join("images", "sesame_bagel_blink.png")).convert_alpha()
	wizard_bagel1 = pygame.image.load(os.path.join("images", "wizard_bagel1.png")).convert_alpha()
	wizard_bagel2 = pygame.image.load(os.path.join("images", "wizard_bagel2.png")).convert_alpha()
	wizard_bagel3 = pygame.image.load(os.path.join("images", "wizard_bagel3.png")).convert_alpha()
	wizard_bagel1_blink = pygame.image.load(os.path.join("images", "wizard_bagel1_blink.png")).convert_alpha()
	wizard_bagel2_blink = pygame.image.load(os.path.join("images", "wizard_bagel2_blink.png")).convert_alpha()
	wizard_bagel3_blink = pygame.image.load(os.path.join("images", "wizard_bagel3_blink.png")).convert_alpha()
	cow_bagel = pygame.image.load(os.path.join("images", "cow_bagel.png")).convert_alpha()
	cow_bagel_blink = pygame.image.load(os.path.join("images", "cow_bagel_blink.png")).convert_alpha()
	everything_bagel = pygame.image.load(os.path.join("images", "everything_bagel.png")).convert_alpha()
	everything_bagel_blink = pygame.image.load(os.path.join("images", "everything_bagel_blink.png")).convert_alpha()
	everything_bagel_shooting = pygame.image.load(os.path.join("images", "everything_bagel_shooting.png")).convert_alpha()
	everything_bagel_shooting_blink = pygame.image.load(os.path.join("images", "everything_bagel_shooting_blink.png")).convert_alpha()
	crais_bagel = pygame.image.load(os.path.join("images", "cinnamon_raisin.png")).convert_alpha()
	crais_bagel_blink = pygame.image.load(os.path.join("images", "cinnamon_raisin_blink.png")).convert_alpha()
	multigrain = pygame.image.load(os.path.join("images", "multigrain.png")).convert_alpha()
	multigrain_blink = pygame.image.load(os.path.join("images", "multigrain_blink.png")).convert_alpha()
	multigrain_angry = pygame.image.load(os.path.join("images", "multigrain_angry.png")).convert_alpha()
	multigrain_angry_blink = pygame.image.load(os.path.join("images", "multigrain_angry_blink.png")).convert_alpha()
	flagel = pygame.image.load(os.path.join("images", "flagel.png")).convert_alpha()
	flagel_puff1 = pygame.image.load(os.path.join("images", "flagel_puff1.png")).convert_alpha()
	flagel_puff2 = pygame.image.load(os.path.join("images", "flagel_puff2.png")).convert_alpha()
	flagel_blink = pygame.image.load(os.path.join("images", "flagel_blink.png")).convert_alpha()
	mini_bagels = pygame.image.load(os.path.join("images", "mini_bagels.png")).convert_alpha()
	mini_bagels1d = pygame.image.load(os.path.join("images", "mini_bagels1d.png")).convert_alpha()
	mini_bagels2d = pygame.image.load(os.path.join("images", "mini_bagels2d.png")).convert_alpha()
	mini_bagels_blink = pygame.image.load(os.path.join("images", "mini_bagels_blink.png")).convert_alpha()
	cat = pygame.image.load(os.path.join("images", "cat.png")).convert_alpha()
	taco_cat = pygame.image.load(os.path.join("images", "taco_cat.png")).convert_alpha()
	melon_cat = pygame.image.load(os.path.join("images", "melon_cat.png")).convert_alpha()
	weenie_cat = pygame.image.load(os.path.join("images", "weenie_cat.png")).convert_alpha()
	baby_cat = pygame.image.load(os.path.join("images", "baby_cat.png")).convert_alpha()
	ninja_cat = pygame.image.load(os.path.join("images", "ninja_cat.png")).convert_alpha()
	pizza_cat = pygame.image.load(os.path.join("images", "pizza_cat.png")).convert_alpha()
	fondue_cat = pygame.image.load(os.path.join("images", "fondue_cat.png")).convert_alpha()
	cat_eating = pygame.image.load(os.path.join("images", "cat_eating.png")).convert_alpha()
	taco_cat_eating = pygame.image.load(os.path.join("images", "taco_cat_eating.png")).convert_alpha()
	melon_cat_eating = pygame.image.load(os.path.join("images", "melon_cat_eating.png")).convert_alpha()
	weenie_cat_eating = pygame.image.load(os.path.join("images", "weenie_cat_eating.png")).convert_alpha()
	baby_cat_eating = pygame.image.load(os.path.join("images", "baby_cat_eating.png")).convert_alpha()
	ninja_cat_eating = pygame.image.load(os.path.join("images", "ninja_cat_eating.png")).convert_alpha()
	pizza_cat_eating = pygame.image.load(os.path.join("images", "pizza_cat_eating.png")).convert_alpha()
	melon_cat_throw1 = pygame.image.load(os.path.join("images", "melon_cat_throw1.png")).convert_alpha()
	melon_cat_throw2 = pygame.image.load(os.path.join("images", "melon_cat_throw2.png")).convert_alpha()
	pizza_cat_ns = pygame.image.load(os.path.join("images", "pizza_cat_ns.png")).convert_alpha()
	pizza_cat_eating_ns = pygame.image.load(os.path.join("images", "pizza_cat_eating_ns.png")).convert_alpha()
	fondue_cat_eating = pygame.image.load(os.path.join("images", "fondue_cat_eating.png")).convert_alpha()
	bagel_shot = pygame.image.load(os.path.join("images", "bagel_shot.png")).convert_alpha()
	poppy_shot = pygame.image.load(os.path.join("images", "poppy_shot.png")).convert_alpha()
	wizard_shot = pygame.image.load(os.path.join("images", "wizard_shot.png")).convert_alpha()
	sesame_shot = pygame.image.load(os.path.join("images", "sesame_shot.png")).convert_alpha()
	garlic_shot = pygame.image.load(os.path.join("images", "garlic_shot.png")).convert_alpha()
	mini_shot = pygame.image.load(os.path.join("images", "mini_shot.png")).convert_alpha()
	hole_cover = pygame.image.load(os.path.join("images", "hole_cover.png")).convert_alpha()
	first_charge = pygame.image.load(os.path.join("images", "first_charge.png")).convert_alpha()
	second_charge = pygame.image.load(os.path.join("images", "second_charge.png")).convert_alpha()
	remote_control1 = pygame.image.load(os.path.join("images", "remote_control1.png")).convert_alpha()
	remote_control2 = pygame.image.load(os.path.join("images", "remote_control2.png")).convert_alpha()
	melon_cat_shot = pygame.image.load(os.path.join("images", "melon_cat_shot.png")).convert_alpha()
	special_melon = pygame.image.load(os.path.join("images", "special_melon.png")).convert_alpha()
	ninja_cat_rope = pygame.image.load(os.path.join("images", "ninja_cat_rope.png")).convert_alpha()
	rope = pygame.image.load(os.path.join("images", "rope.png")).convert_alpha()
	wheat = pygame.image.load(os.path.join("images", "wheat.png")).convert_alpha()
	fire = pygame.image.load(os.path.join("images", "fire.png")).convert_alpha()
	cage = pygame.image.load(os.path.join("images", "cage.png")).convert_alpha()
	big_cage = pygame.image.load(os.path.join("images", "big_cage.png")).convert_alpha()
	empty_tile = pygame.image.load(os.path.join("images", "empty_tile.png")).convert_alpha()
	fist = pygame.image.load(os.path.join("images", "fist.png")).convert_alpha()
	multigrain_melon = pygame.image.load(os.path.join("images", "multigrain_melon.png")).convert_alpha()
	fist_release = pygame.image.load(os.path.join("images", "fist_release.png")).convert_alpha()
	melon_shot_r = pygame.image.load(os.path.join("images", "melon_shot_r.png")).convert_alpha()
	wizard_shot_r = pygame.image.load(os.path.join("images", "wizard_shot_r.png")).convert_alpha()
	pizza = pygame.image.load(os.path.join("images", "pizza.png")).convert_alpha()
	dog = pygame.image.load(os.path.join("images", "dog.png")).convert_alpha()
	dog_eating = pygame.image.load(os.path.join("images", "dog_eating.png")).convert_alpha()

	# Fonts
	main_font = pygame.font.Font("visitor1.ttf",50)
	wave_font = pygame.font.Font("visitor1.ttf",35)
	exclaimation = main_font.render("!",False,(0,0,0))

	# Sprite Lists
	allSprites = pygame.sprite.Group()
	bagelList = pygame.sprite.Group()
	emptyBList = pygame.sprite.Group()
	bagelCatList = pygame.sprite.Group() # Obsolete
	catList = pygame.sprite.Group()
	bulletList = pygame.sprite.Group()
	catBulletList = pygame.sprite.Group()
	wheatList = pygame.sprite.Group()
	ghostBagelList = pygame.sprite.Group()
	emptyCowBList = pygame.sprite.Group()
	cageList = pygame.sprite.Group()
	dogList = pygame.sprite.Group()
	explosionList = pygame.sprite.Group()
	trailList = pygame.sprite.Group()

	# hasBagel
	page = 1
	hasBagel = "null"

	# Bagel Recharging
	plainRecharge = False
	wheatRecharge = False
	poppyRecharge = False
	sesameRecharge = False
	wizardRecharge = False
	cowRecharge = False
	everyRecharge = False
	craisRecharge = False
	multiRecharge = False
	flagelRecharge = False
	miniRecharge = False
	plainRechargeTime = 0
	wheatRechargeTime = 0
	poppyRechargeTime = 0
	sesameRechargeTime = 0
	wizardRechargeTime = 0
	cowRechargeTime = 0
	everyRechargeTime = 0
	craisRechargeTime = 0
	multiRechargeTime = 0
	flagelRechargeTime = 0
	miniRechargeTime = 0

	plainCapacity = 200
	wheatCapacity = 425
	poppyCapacity = 600
	sesameCapacity = 600
	wizardCapacity = 375
	cowCapacity = 600
	everyCapacity = 425
	craisCapacity = 600
	multiCapacity = 600
	flagelCapacity = 900
	miniCapacity = 75

	# spawnCats
	preGame = True
	preGameTime = 0
	spawnTime = 0
	waveTime = 0
	wave = 1
	catNumber = 1
	preCatList = []
	instances = 1
	catTypes = ["cat","cat","cat","cat","cat","cat"]
	ninja_cat_rope_list = []
	rope_list = []
	extinction = [0] # I hate this variable...

	# Wave Stuff
	wavePercentRaw = 0
	wavePercent = 0
	waveBar = 0

	# Wheat
	wheatCount = 5
	plainCost = 1
	wheatCost = 2
	poppyCost = 4
	sesameCost = 6
	wizardCost = 5
	cowCost = 8
	everyCost = 3
	craisCost = 4
	multiCost = 5
	flagelCost = 6
	miniCost = 1
	wheatMoveList = []

	# Danger! variables
	exclaim = True
	drawDanger = 0
	dangerTimer = 0
	dangerAlpha = 2
	dangerTurn = 0

	# Mouse Stuff
	lastClick = None
	nextClick = None

	# You're a cow!
	milk = 0

	# Computer selecting
	selecting = False

	def eventProcess(self):
		global particle_list, paused, pos
		for event in pygame.event.get():
			if (event.type == pygame.QUIT) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN and self.gameOver == False and self.titleOn == False:
				pos = pygame.mouse.get_pos()
				if event.key == pygame.K_p:
					paused = not paused
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					if not self.selecting:
						self.selecting = True
					pos = pygame.mouse.get_pos()
					pygame.mouse.set_pos([pos[0],pos[1] - 66])
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					if not self.selecting:
						self.selecting = True
					pos = pygame.mouse.get_pos()
					pygame.mouse.set_pos([pos[0],pos[1] + 66])
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					if not self.selecting:
						self.selecting = True
					pos = pygame.mouse.get_pos(9)
					pygame.mouse.set_pos([pos[0] - 66,pos[1]])
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					if not self.selecting:
						self.selecting = True
					pos = pygame.mouse.get_pos()
					pygame.mouse.set_pos([pos[0] + 66,pos[1]])
				if event.key == pygame.K_u:
					self.selecting = False
					pygame.mouse.set_visible(True)
				if event.key == pygame.K_TAB:
					if self.page == 1:
						self.page = 2
					elif self.page == 2:
						self.page = 3
					elif self.page == 3:
						self.page = 1
					self.hasBagel = "null"
				if event.key == pygame.K_SPACE:
					for i in self.wheatList:
						bullet_vec_x = i.rect.x - 145
						bullet_vec_y = i.rect.y - 405
						vec_length = math.sqrt(bullet_vec_x ** 2 + bullet_vec_y ** 2)
						bullet_vec_x = (bullet_vec_x / vec_length) * 13
						bullet_vec_y = (bullet_vec_y / vec_length) * 13
						self.wheatMoveList.append([bullet_vec_x,bullet_vec_y,i.rect.x,i.rect.y])
						i.kill()
						i.remove()
						self.wheatCount += 1
				"""if event.key == pygame.K_BACKQUOTE:
					for i in self.bagelList:
						if i.rect.collidepoint(pos[0],pos[1]):
							if i.bagelType != "cow":   # Fix
								if i.bagelType == "wheat" or i.bagelType == "crais":
									particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (156,111,40), 40, 25, None)
								elif i.bagelType == "multi":
									particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (172,102,45), 40, 25, None)
								elif i.bagelType == "wizard":
									particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (229,218,165), 40, 36, None)
								else:
									particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (229,218,165), 40, 25, None)
							else:
								particle_list = self.create_particles(particle_list, (i.rect.x + 60,i.rect.y + 33), (229,218,165), 40, 25, None)
							if android:
								android.vibrate(0.05)
							i.health = 0
							if self.particleSetting == False:
								self.fork.play()
							self.hasBagel = "null" """
				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					for i in self.bagelList:
						if i.bagelType == "cow" and i.sleepTimer > 0 and i.milkLeft > 0 and self.milk < 40:
							self.milk += 1
							i.milkLeft -= 1

				# Functions for selecting

				if self.selecting == True:
					pos = pygame.mouse.get_pos()
					for i in self.emptyBList:
						if i.rect.collidepoint(pos[0],pos[1]):
							if self.page == 1:
								if event.key == pygame.K_1 and self.wheatRecharge == False and self.hasBagel != "wheat" and (self.wheatCount >= self.wheatCost):
									self.hasBagel = "wheat"
									self.clicked = True
								if event.key == pygame.K_2 and self.plainRecharge == False and self.hasBagel != "plain" and (self.wheatCount >= self.plainCost):
									self.hasBagel = "plain"
									self.clicked = True
								if event.key == pygame.K_3 and self.poppyRecharge == False and self.hasBagel != "poppy" and (self.wheatCount >= self.poppyCost):
									self.hasBagel = "poppy"
									self.clicked = True
								if event.key == pygame.K_4 and self.sesameRecharge == False and self.hasBagel != "sesame" and (self.wheatCount >= self.sesameCost):
									self.hasBagel = "sesame"
									self.clicked = True
								if event.key == pygame.K_5 and self.wizardRecharge == False and self.hasBagel != "wizard" and (self.wheatCount >= self.wizardCost):
									self.hasBagel = "wizard"
									self.clicked = True
							elif self.page == 2:
								if event.key == pygame.K_1 and self.cowRecharge == False and self.hasBagel != "cow" and (self.wheatCount >= self.cowCost):
									self.hasBagel = "cow"
									self.clicked = True
								if event.key == pygame.K_2 and self.everyRecharge == False and self.hasBagel != "everything" and (self.wheatCount >= self.everyCost):
									self.hasBagel = "everything"
									self.clicked = True
								if event.key == pygame.K_3 and self.craisRecharge == False and self.hasBagel != "crais" and (self.wheatCount >= self.craisCost):
									self.hasBagel = "crais"
									self.clicked = True
								if event.key == pygame.K_4 and self.multiRecharge == False and self.hasBagel != "multi" and (self.wheatCount >= self.multiCost):
									self.hasBagel = "multi"
									self.clicked = True
								if event.key == pygame.K_5 and self.flagelRecharge == False and self.hasBagel != "flagel" and (self.wheatCount >= self.flagelCost):
									self.hasBagel = "flagel"
									self.clicked = True
							elif self.page == 3:
								if event.key == pygame.K_1 and self.miniRecharge == False and self.hasBagel != "mini" and (self.wheatCount >= self.miniCost):
									self.hasBagel = "mini"
									self.clicked = True

					for i in self.bagelList:
						if i.rect.collidepoint(pos[0],pos[1]) and i.bagelType == "wizard" and i.level < 3:
							if event.key == pygame.K_5 and self.wizardRecharge == False and self.hasBagel != "wizard" and (self.wheatCount >= self.wizardCost):
								self.wheatCount -= self.wizardCost
								i.level += 1
								i.levelUp = True
								particle_list = self.create_particles(particle_list, (i.rect.x + 30,i.rect.y), (232,221,29), 40, 57, "exp")
								if i.level == 2:
									i.image = self.wizard_bagel2
								elif i.level == 3:
									i.image = self.wizard_bagel3
								self.wizardRecharge = True
								self.hasBagel = "null"
							elif i.rect.collidepoint(pos[0],pos[1]) and (i.bagelType != "wizard" or i.level >= 3):
								self.clicked = False
						if i.rect.collidepoint(pos[0],pos[1]):
							if event.key == pygame.K_6:
								if i.bagelType != "cow" and self.milk >= 20: # probably not necessary but hey
									i.cheeseItUp = 400
									self.milk -= 20
									self.hasBagel = "null"
							if event.key == pygame.K_BACKQUOTE:
								if i.bagelType != "cow":   # Fix
									if i.bagelType == "wheat" or i.bagelType == "crais":
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (156,111,40), 40, 25, None)
									elif i.bagelType == "multi":
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (172,102,45), 40, 25, None)
									elif i.bagelType == "wizard":
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (229,218,165), 40, 36, None)
									else:
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (229,218,165), 40, 25, None)
								else:
									particle_list = self.create_particles(particle_list, (i.rect.x + 60,i.rect.y + 33), (229,218,165), 40, 25, None)
								if android:
									android.vibrate(0.05)
								i.health = 0
								if self.particleSetting == False:
									self.fork.play()
								self.hasBagel = "null"

			#if event.type == pygame.MOUSEMOTION:

			if event.type == pygame.MOUSEBUTTONDOWN and (paused == False and self.gameOver == False):
				pos = pygame.mouse.get_pos()
				#print(pos[0],pos[1])
				if self.titleOn == True:
					if self.play_button.collidepoint(pos[0],pos[1]):
						self.titleOn = False
					if self.options_button_menu.collidepoint(pos[0],pos[1]):
						paused = True
						self.options = True
					if self.info_button.collidepoint(pos[0],pos[1]):
						paused = True
						self.info = True

				if self.titleOn == False:
					# Cows cows cows cows cows cows cows cows
					for i in self.bagelList:
						if i.bagelType == "cow" and i.rect.collidepoint(pos[0],pos[1]) and i.sleepTimer > 0 and i.milkLeft > 0 and self.milk < 40:
							self.milk += 1
							i.milkLeft -= 1

					if self.wheatmilk_box.collidepoint(pos[0],pos[1]) and self.hasBagel != "creamcheese" and self.milk >= 20:
						self.hasBagel = "creamcheese"
					elif self.wheatmilk_box.collidepoint(pos[0],pos[1]) and self.hasBagel == "creamcheese" and self.milk >= 20:
						self.hasBagel = "null"

					# Pause box ooooh yes
					if self.menu_button.collidepoint(pos[0],pos[1]):
						paused = not paused

					if self.arrow_button.collidepoint(pos[0],pos[1]):
						if self.page == 1:
							self.page = 2
						elif self.page == 2:
							self.page = 3
						elif self.page == 3:
							self.page = 1
						self.hasBagel = "null"

					# Check for box collisions

					if self.page == 1:
						if self.box1.collidepoint(pos[0],pos[1]) and self.wheatRecharge == False and self.hasBagel != "wheat" and (self.wheatCount >= self.wheatCost):
							self.hasBagel = "wheat"
						elif self.box1.collidepoint(pos[0],pos[1]) and self.wheatRecharge == False and self.hasBagel == "wheat" and (self.wheatCount >= self.wheatCost):
							self.hasBagel = "null"

						if self.box2.collidepoint(pos[0],pos[1]) and self.plainRecharge == False and self.hasBagel != "plain" and (self.wheatCount >= self.plainCost):
							self.hasBagel = "plain"
						elif self.box2.collidepoint(pos[0],pos[1]) and self.plainRecharge == False and self.hasBagel == "plain" and (self.wheatCount >= self.plainCost):
							self.hasBagel = "null"

						if self.box3.collidepoint(pos[0],pos[1]) and self.poppyRecharge == False and self.hasBagel != "poppy" and (self.wheatCount >= self.poppyCost):
							self.hasBagel = "poppy"
						elif self.box3.collidepoint(pos[0],pos[1]) and self.poppyRecharge == False and self.hasBagel == "poppy" and (self.wheatCount >= self.poppyCost):
							self.hasBagel = "null"

						if self.box4.collidepoint(pos[0],pos[1]) and self.sesameRecharge == False and self.hasBagel != "sesame" and (self.wheatCount >= self.sesameCost):
							self.hasBagel = "sesame"
						elif self.box4.collidepoint(pos[0],pos[1]) and self.sesameRecharge == False and self.hasBagel == "sesame" and (self.wheatCount >= self.sesameCost):
							self.hasBagel = "null"

						if self.box5.collidepoint(pos[0],pos[1]) and self.wizardRecharge == False and self.hasBagel != "wizard" and (self.wheatCount >= self.wizardCost):
							self.hasBagel = "wizard"
						elif self.box5.collidepoint(pos[0],pos[1]) and self.wizardRecharge == False and self.hasBagel == "wizard" and (self.wheatCount >= self.wizardCost):
							self.hasBagel = "null"

					elif self.page == 2:
						if self.box1.collidepoint(pos[0],pos[1]) and self.cowRecharge == False and self.hasBagel != "cow" and (self.wheatCount >= self.cowCost):
							self.hasBagel = "cow"
						elif self.box1.collidepoint(pos[0],pos[1]) and self.cowRecharge == False and self.hasBagel == "cow" and (self.wheatCount >= self.cowCost):
							self.hasBagel = "null"

						if self.box2.collidepoint(pos[0],pos[1]) and self.everyRecharge == False and self.hasBagel != "everything" and (self.wheatCount >= self.everyCost):
							self.hasBagel = "everything"
						elif self.box2.collidepoint(pos[0],pos[1]) and self.everyRecharge == False and self.hasBagel == "everything" and (self.wheatCount >= self.everyCost):
							self.hasBagel = "null"

						if self.box3.collidepoint(pos[0],pos[1]) and self.craisRecharge == False and self.hasBagel != "crais" and (self.wheatCount >= self.craisCost):
							self.hasBagel = "crais"
						elif self.box3.collidepoint(pos[0],pos[1]) and self.craisRecharge == False and self.hasBagel == "crais" and (self.wheatCount >= self.craisCost):
							self.hasBagel = "null"

						if self.box4.collidepoint(pos[0],pos[1]) and self.multiRecharge == False and self.hasBagel != "multi" and (self.wheatCount >= self.multiCost):
							self.hasBagel = "multi"
						elif self.box4.collidepoint(pos[0],pos[1]) and self.multiRecharge == False and self.hasBagel == "multi" and (self.wheatCount >= self.multiCost):
							self.hasBagel = "null"

						if self.box5.collidepoint(pos[0],pos[1]) and self.flagelRecharge == False and self.hasBagel != "flagel" and (self.wheatCount >= self.flagelCost):
							self.hasBagel = "flagel"
						elif self.box5.collidepoint(pos[0],pos[1]) and self.flagelRecharge == False and self.hasBagel == "flagel" and (self.wheatCount >= self.flagelCost):
							self.hasBagel = "null"

					elif self.page == 3:
						if self.box1.collidepoint(pos[0],pos[1]) and self.miniRecharge == False and self.hasBagel != "mini" and (self.wheatCount >= self.miniCost):
							self.hasBagel = "mini"
						elif self.box1.collidepoint(pos[0],pos[1]) and self.miniRecharge == False and self.hasBagel == "mini" and (self.wheatCount >= self.miniCost):
							self.hasBagel = "null"

					# This is separate

					if (self.hasBagel != "null") and (self.box1.collidepoint(pos[0],pos[1]) or self.box2.collidepoint(pos[0],pos[1]) or self.box3.collidepoint(pos[0],pos[1]) or self.box4.collidepoint(pos[0],pos[1]) or self.box5.collidepoint(pos[0],pos[1])) == False:
						for i in self.bagelList:
							if i.rect.collidepoint(pos[0],pos[1]):
								self.clicked = False

						for i in self.emptyBList:
							if i.rect.collidepoint(pos[0],pos[1]):
								if len(self.wheatList) > 0:
									for k in self.wheatList:
										if not k.rect.collidepoint(pos[0],pos[1]):
											self.clicked = True
								else:
									self.clicked = True

					for i in self.wheatList:
						if i.rect.collidepoint(pos[0],pos[1]):
							bullet_vec_x = i.rect.x - 145
							bullet_vec_y = i.rect.y - 405
							vec_length = math.sqrt(bullet_vec_x ** 2 + bullet_vec_y ** 2)
							bullet_vec_x = (bullet_vec_x / vec_length) * 13
							bullet_vec_y = (bullet_vec_y / vec_length) * 13
							self.wheatMoveList.append([bullet_vec_x,bullet_vec_y,i.rect.x,i.rect.y])
							i.kill()
							i.remove()
							self.wheatCount += 1

					# ... then fork collisions

					if self.forkBox.collidepoint(pos[0],pos[1]):
						if self.hasBagel != "fork":
							self.hasBagel = "fork"
						elif self.hasBagel == "fork":
							self.hasBagel = "null"

					if self.hasBagel == "fork":
						for i in self.bagelList:
							if i.rect.collidepoint(pos[0],pos[1]):
								if i.bagelType != "cow":   # Fix
									if i.bagelType == "wheat" or i.bagelType == "crais":
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (156,111,40), 40, 25, None)
									elif i.bagelType == "multi":
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (172,102,45), 40, 25, None)
									elif i.bagelType == "wizard":
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (229,218,165), 40, 36, None)
									else:
										particle_list = self.create_particles(particle_list, (i.rect.x + 25,i.rect.y + 21), (229,218,165), 40, 25, None)
								else:
									particle_list = self.create_particles(particle_list, (i.rect.x + 60,i.rect.y + 33), (229,218,165), 40, 25, None)
								if android:
									android.vibrate(0.05)
								i.health = 0
								if self.particleSetting == False:
									self.fork.play()
								self.hasBagel = "null"

					if self.hasBagel == "creamcheese":
						for i in self.bagelList:
							if i.rect.collidepoint(pos[0],pos[1]):
								if i.bagelType != "cow" and self.milk >= 20: # probably not necessary but hey
									i.cheeseItUp = 400
									self.milk -= 20
									self.hasBagel = "null" 


					# Wizard Bagels!
					if self.hasBagel == "wizard":
						for i in self.bagelList:
							if i.rect.collidepoint(pos[0],pos[1]) and i.bagelType == "wizard" and i.level < 3:
								self.wheatCount -= self.wizardCost
								i.level += 1
								i.levelUp = True
								particle_list = self.create_particles(particle_list, (i.rect.x + 30,i.rect.y), (232,221,29), 40, 57, "exp")
								if i.level == 2:
									i.image = self.wizard_bagel2
								elif i.level == 3:
									i.image = self.wizard_bagel3
								self.wizardRecharge = True
								self.hasBagel = "null"

							elif i.rect.collidepoint(pos[0],pos[1]) and (i.bagelType != "wizard" or i.level >= 3):
								self.clicked = False

			elif event.type == pygame.MOUSEBUTTONDOWN and paused == True:
				pos = pygame.mouse.get_pos()
				#print(pos[0])
				if self.resume_button.collidepoint(pos[0],pos[1]) and self.options == False and self.info == False:
					paused = False
					#self.loadGame()
					# For recording purposes
					"""position = random.randrange(11,394,66)
					cat = Cat("cat",10,265,143,self.cat,self.cat_eating)
					cat.move = False
					cat.storedY = position
					cat.add(self.catList)
					cat.add(self.bagelCatList)
					cat.add(self.allSprites)"""
					# Savin' them sound values on resume
					with open('save.dat','wb') as fp:
						pickle.dump(self.music_slider_value,fp)
						pickle.dump(self.sound_slider_value,fp)
						pickle.dump(self.musicOff,fp)
						pickle.dump(self.soundOff,fp)
				elif self.quit_button.collidepoint(pos[0],pos[1]) and self.options == False and self.info == False:
					self.titleOn = True
					self.restartGame()
				elif self.restart_button.collidepoint(pos[0],pos[1]) and self.options == False and self.info == False:
					#self.saveGame()
					self.restartGame()
				elif self.options_button.collidepoint(pos[0],pos[1]) and self.options == False and self.info == False:
					self.options = True
				elif self.music_button.collidepoint(pos[0],pos[1]) and self.options == True and self.info == False:
					self.musicOff = not self.musicOff
				elif self.sound_button.collidepoint(pos[0],pos[1]) and self.options == True and self.info == False :
					self.soundOff = not self.soundOff
				elif self.options_back.collidepoint(pos[0],pos[1]) and self.options == True and self.info == False:
					self.options = False
					if self.titleOn == True:
						paused = False
				elif self.particles_button.collidepoint(pos[0],pos[1]) and self.options == True and self.info == False:
					self.particleSetting = not self.particleSetting
				elif self.info == True and self.options == False:
					if self.info_back.collidepoint(pos[0],pos[1]):
						self.info = False
						paused = False
					elif self.wiki_info.collidepoint(pos[0],pos[1]):
						# One day this will work...
						webbrowser.open('http://bagels-vs-cats.wikia.com/wiki/Bagels_vs._Cats_Wikia')

			elif event.type == pygame.MOUSEBUTTONDOWN and self.gameOver == True:
				pos = pygame.mouse.get_pos()
				if self.game_over_restart_button.collidepoint(pos[0],pos[1]):
					self.restartGame()
					self.gameOver = False

		if pygame.mouse.get_pressed()[0] != 0:
			pos = pygame.mouse.get_pos()
			# Music
			if self.music_slider_value < 0:
				self.music_slider_value = 0
			if self.music_slider_value > 184:
				self.music_slider_value = 184
			if self.music_slider_button.collidepoint(pos[0],pos[1]) and self.options == True:
				self.music_slider_value = pos[0] - 296
			# Sound
			if self.sound_slider_value < 0:
				self.sound_slider_value = 0
			if self.sound_slider_value > 184:
				self.sound_slider_value = 184
			if self.sound_slider_button.collidepoint(pos[0],pos[1]) and self.options == True:
				self.sound_slider_value = pos[0] - 296

		return True

	def titleScreen(self):
		if self.titleOn == True:
			screen.blit(self.title_screen,(0,0))
			screen.blit(self.version,(490,450))
			"""if self.firstPress == True:
				screen.blit(self.pressed_play_button,(281,178))"""

	def drawBackground(self):
		if self.titleOn == False:
			wheat_amount = self.main_font.render(str(self.wheatCount),False,(0,0,0))
			wave_count = self.wave_font.render("Wave " + str(self.wave),False,(0,0,0))
			"""wave_count.unlock()
			wave_count.set_alpha(180)"""
			text_width = wheat_amount.get_width()
			text_height = wheat_amount.get_height()
			screen.fill((255,255,255))
			screen.blit(self.grass,(0,0))
			for row in range(6):
				for column in range(2):
					screen.blit(self.blank_tile_dirt,(column*66, row*66))
			for row in range(6):
				for column in range(11):
					screen.blit(self.tile,(column*66 + 132,row*66))
			for i in self.bagelList:
				if i.cheeseItUp > 0:
					screen.blit(self.cream_cheese_tile,(i.storedx,i.storedy))
			if self.selecting == True:
				pygame.mouse.set_visible(False)
			if self.displayWave == 0:
				screen.blit(wave_count,(665,10))

			screen.blit(self.arrows,(748,412))

			if self.drawDanger != 0:
				dangerRect = pygame.Surface((800,70))
				dangerRect.set_alpha(self.dangerAlpha)
				dangerRect.fill((255,0,0))
				screen.blit(dangerRect,(0,self.drawDanger - 11))
				if paused == False:
					if self.dangerTurn < 2:
						self.dangerTimer += 1
						if self.dangerTimer < 70:
							self.dangerAlpha += 1
						elif 100 > self.dangerTimer >= 70:
							self.dangerAlpha -= 1
						elif self.dangerTimer >= 100:
							self.dangerTimer = 0
							self.dangerTurn += 1
					elif self.dangerTurn == 2:
						self.dangerAlpha -= 1						
						if self.dangerAlpha == 0:
							self.drawDanger = 0

			# Recharge Stuff
			plainBar = round(42 * (self.plainRechargeTime / self.plainCapacity))
			wheatBar = round(42 * (self.wheatRechargeTime / self.wheatCapacity))
			poppyBar = round(42 * (self.poppyRechargeTime / self.poppyCapacity))
			sesameBar = round(42 * (self.sesameRechargeTime / self.sesameCapacity))
			wizardBar = round(42 * (self.wizardRechargeTime / self.wizardCapacity))
			cowBar = round(42 * (self.cowRechargeTime / self.cowCapacity))
			everyBar = round(42 * (self.everyRechargeTime / self.everyCapacity))
			craisBar = round(42 * (self.craisRechargeTime / self.craisCapacity))
			multiBar = round(42 * (self.multiRechargeTime / self.multiCapacity))
			flagelBar = round(42 * (self.flagelRechargeTime / self.flagelCapacity))
			miniBar = round(42 * (self.miniRechargeTime / self.miniCapacity))

			if self.page == 1:
				if self.wheatRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(220,410,100,50))
				elif self.wheatRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(220,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(224,414,92,wheatBar))

				if self.plainRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(325,410,100,50))
				elif self.plainRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(325,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(329,414,92,plainBar))

				if self.poppyRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(430,410,100,50))
				elif self.poppyRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(430,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(434,414,92,poppyBar))

				if self.sesameRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(535,410,100,50))
				elif self.sesameRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(535,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(539,414,92,sesameBar))

				if self.wizardRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(640,410,100,50))
				elif self.wizardRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(640,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(644,414,92,wizardBar))

				screen.blit(self.wheat_backing,(220,410))
				screen.blit(self.plain_backing,(325,410))
				screen.blit(self.poppy_backing,(430,410))
				screen.blit(self.sesame_backing,(535,410))
				screen.blit(self.wizard_backing,(640,410))

			elif self.page == 2:
				if self.cowRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(220,410,100,50))
				elif self.cowRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(220,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(224,414,92,cowBar))

				if self.everyRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(325,410,100,50))
				elif self.everyRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(325,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(329,414,92,everyBar))

				if self.craisRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(430,410,100,50))
				elif self.craisRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(430,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(434,414,92,craisBar))

				if self.multiRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(535,410,100,50))
				elif self.multiRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(535,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(539,414,92,multiBar))

				if self.flagelRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(640,410,100,50))
				elif self.flagelRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(640,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(644,414,92,flagelBar))

				screen.blit(self.cow_backing,(220,410))
				screen.blit(self.every_backing,(325,410))
				screen.blit(self.crais_backing,(430,410))
				screen.blit(self.multi_backing,(535,410))
				screen.blit(self.flagel_backing,(640,410))

			elif self.page == 3:
				if self.miniRecharge == False:
					pygame.draw.rect(screen,(255,255,255),(220,410,100,50))
				elif self.miniRecharge == True:
					pygame.draw.rect(screen,(64,193,225),(220,410,100,50))
					pygame.draw.rect(screen,(255,255,255),(224,414,92,miniBar))

				screen.blit(self.mini_backing,(220,410))

			# Forks

			if self.hasBagel == "fork":
				screen.blit(self.fork_overlay,(70,400))

			# Bagel Selection

			if self.page == 1:
				if self.hasBagel == "wheat":
					screen.blit(self.selected,(220,410))
				if self.hasBagel == "plain":
					screen.blit(self.selected,(325,410))
				if self.hasBagel == "poppy":
					screen.blit(self.selected,(430,410))
				if self.hasBagel == "sesame":
					screen.blit(self.selected,(535,410))
				if self.hasBagel == "wizard":
					screen.blit(self.selected,(640,410))

			elif self.page == 2:
				if self.hasBagel == "cow":
					screen.blit(self.selected,(220,410))
				if self.hasBagel == "everything":
					screen.blit(self.selected,(325,410))
				if self.hasBagel == "crais":
					screen.blit(self.selected,(430,410))
				if self.hasBagel == "multi":
					screen.blit(self.selected,(535,410))
				if self.hasBagel == "flagel":
					screen.blit(self.selected,(640,410))

			elif self.page == 3:
				if self.hasBagel == "mini":
					screen.blit(self.selected,(220,410))

			# Gray out boxes

			if self.page == 1:
				if self.wheatCost > self.wheatCount:
					screen.blit(self.locked,(220,410))
				if self.plainCost > self.wheatCount:
					screen.blit(self.locked,(325,410))
				if self.poppyCost > self.wheatCount:
					screen.blit(self.locked,(430,410))
				if self.sesameCost > self.wheatCount:
					screen.blit(self.locked,(535,410))
				if self.wizardCost > self.wheatCount:
					screen.blit(self.locked,(640,410))

			elif self.page == 2:
				if self.cowCost > self.wheatCount:
					screen.blit(self.locked,(220,410))
				if self.everyCost > self.wheatCount:
					screen.blit(self.locked,(325,410))
				if self.craisCost > self.wheatCount:
					screen.blit(self.locked,(430,410))
				if self.multiCost > self.wheatCount:
					screen.blit(self.locked,(535,410))
				if self.flagelCost > self.wheatCount:
					screen.blit(self.locked,(640,410))

			elif self.page == 3:
				if self.miniCost > self.wheatCount:
					screen.blit(self.locked,(220,410))

			# Milk and wheat
			milkPercent = self.milk / 40
			milkPercentRaw = 60 * milkPercent
			milkBar = round(milkPercentRaw)
			if self.milk > 0:
				pygame.draw.rect(screen,(255,255,255),(145,465,60,-milkBar))

			if self.milk >= 20:
				screen.blit(self.milk_ready,(140,400))
			if self.hasBagel == "creamcheese":
				screen.blit(self.cream_cheese_selected,(140,400))

			for i in self.emptyBList: # A bit out of place but that's OK
				if i.bagelSelected == True:
					screen.blit(self.selector,(i.rect.x,i.rect.y))
			for i in self.bagelList:
				if i.bagelSelected == True:
					screen.blit(self.selector,(i.storedx,i.storedy))

			screen.blit(wheat_amount,(178 - (text_width/2),435 - (text_height/2)))
			if self.lightBox > 0:
				screen.blit(self.wheat_shine,(140,400))
				self.lightBox -= 1

			# Numbered Selector Mode
			if self.selecting == True:
				screen.blit(self.numbered_sel,(306,446))

			# Wave bar
			self.wavePercent = self.waveTime / 3600
			self.wavePercentRaw = 800 * self.wavePercent
			self.waveBar = round(self.wavePercentRaw)
			pygame.draw.rect(screen,(255,0,0),(0,470,self.waveBar,10))
			#screen.blit(self.tile, (0,0))

	def drawSprites(self):
		global particle_list

		# Drawing starts
		for i in self.catList:
			if i.caged or i.catType == "baby_cat":
				i.draw(screen)
		self.trailList.draw(screen)
		self.bagelList.draw(screen)
		self.bulletList.draw(screen)
		self.dogList.draw(screen)
		self.catBulletList.draw(screen)
		for i in self.cageList:
			if i.dogInside == True:
				screen.blit(self.dog,(i.rect.x + 11,i.rect.y + 8))
		self.cageList.draw(screen)
		self.ghostBagelList.draw(screen)
		self.explosionList.draw(screen)

		for i in self.bagelList:
			if i.bagelType == "crais" and (paused == False and self.gameOver == False):
					i.dropIt(self.cage,self.catList,self.allSprites,self.cageList)
					if i.fired == True:
						if i.fireTimer < 50:
							screen.blit(self.exclaimation,(i.rect.x + 25, i.rect.y - 37))
						elif 373 >= i.fireTimer >= 50:
							screen.blit(self.remote_control1,(i.rect.x + 49, i.rect.y + 10))
						elif i.fireTimer >= 374:
							i.remoteTimer += 1
						if 25 >= i.remoteTimer >= 1:
							screen.blit(self.remote_control2,(i.rect.x + 49, i.rect.y + 10))
							i.remoteTimer += 1  
						elif i.remoteTimer > 25:
							i.remoteTimer = 0

		for k in self.catList:
			if not k.caged:
				k.draw(screen)
			if k.gameOver == True:
				self.gameOver = True
				self.paused = False

		for i in self.bagelList:
			if i.bagelType == "multi":
				if 0 < i.fistTimer <= 24:
					screen.blit(self.fist,(i.rect.x + 49, i.rect.y + 14))
					if i.fistTimer == 24:
						particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y), (187,187,187), 5, 45, None)
						if self.particleSetting == False:
							self.punch.play()
				elif i.fistTimer <= 0:
					i.fistTimer = 25

				if i.holdMelon:
					i.holdMelonTimer -= 1
					if i.holdMelonTimer >= 80:
						screen.blit(self.multigrain_melon,(i.rect.x + 47, i.rect.y -8))
					elif 0 < i.holdMelonTimer < 80:
						screen.blit(self.fist_release,(i.rect.x + 49, i.rect.y + 9))
						if i.holdMelonTimer == 79:
							if i.cheeseItUp > 0:
								bullet = Bullet(i.rect.x + 58, i.rect.y + 11, self.melon_shot_r, "melon_r_thru", 40, 0, False)
								bullet.add(self.bulletList)
								bullet.add(self.allSprites)
								bullet.speed = 9
							else:
								bullet = Bullet(i.rect.x + 58, i.rect.y + 11, self.melon_shot_r, "melon_r", 15, 0, False)
								bullet.add(self.bulletList)
								bullet.add(self.allSprites)
								bullet.speed = 6

					elif i.holdMelonTimer <= 0:
						i.holdMelonTimer = 200
						i.holdMelon = False

			"""if i.bagelType == "wizard" and i.exp_list != None:
				for j in i.exp_list:
					if j[1] < i.rect.y + 61:
						j[1] += 1
					pygame.draw.rect(screen,(11,232,0),(j[0],j[1],5,5))"""

			"""if i.bagelType == "wizard":
				if i.levelUp == True:
					for j in range(20):
						x = random.randrange(i.rect.x,i.rect.x + 61)
						y = random.randrange(i.rect.y - 30,i.rect.y + 61)
						i.exp_list.append([x,y])
					i.levelUp = False
				for k in i.exp_list:
					if k[1] < i.rect.y + 61:
						k[1] += 1
					pygame.draw.rect(screen,(11,232,0),(k[0],k[1],5,5))"""

		# Drawing ends

		# Separate updating stuff because pause button is broke
		self.bagelList.update()
		self.dogList.update(paused)
		self.catBulletList.update(paused)
		self.wheatList.update(paused)
		self.bulletList.update(paused)
		self.cageList.update(paused,self.big_cage,self.dog,self.dog_eating,self.dogList)
		self.catList.update(paused)
		self.ghostBagelList.update()
		self.explosionList.update()
		self.trailList.update()


		for i in self.cageList:
			if i.stopped == True and i.disTimer == 2:
				particle_list = self.create_particles(particle_list, (i.rect.x + 50, i.rect.y + 29), (117,66,0), 40, 25, None)
				if self.particleSetting == False:
					self.cageDrop.play()

		for i in self.bagelList:
			i.destroy(self.bagelList,self.emptyBList,self.emptyCowBList)
			if paused == False:
				if i.bagelType == "plain" and self.gameOver == False:
					i.fire(self.bagel_shot,self.bulletList,self.allSprites,self.catList,self.poppy_shot,self.sesame_shot,self.garlic_shot,self.mini_shot)
					if 53 <= i.fireTimer <= 60 and i.fired == True:
						screen.blit(self.hole_cover,(i.rect.x + 21, i.rect.y + 13))
				elif i.bagelType == "poppy" and self.gameOver == False:
					i.fire(self.poppy_shot,self.bulletList,self.allSprites,self.catList,self.poppy_shot,self.sesame_shot,self.garlic_shot,self.mini_shot)
				elif i.bagelType == "wizard" and self.gameOver == False:
					i.fire(self.wizard_shot,self.bulletList,self.allSprites,self.catList,self.poppy_shot,self.sesame_shot,self.garlic_shot,self.mini_shot)
					# Charge stuff here
					if i.fired == True:
						if 150 > i.fireTimer >= 50:
							screen.blit(self.first_charge,(i.rect.x + 17, i.rect.y + 27)) #24,15
						elif 200 > i.fireTimer >= 150:
							screen.blit(self.second_charge,(i.rect.x + 17, i.rect.y + 27)) #22,13
				elif i.bagelType == "everything" and self.gameOver == False:
					i.fire(self.poppy_shot,self.bulletList,self.allSprites,self.catList,self.poppy_shot,self.sesame_shot,self.garlic_shot,self.mini_shot)
				elif i.bagelType == "multi" and self.gameOver == False:
					i.fire(self.poppy_shot,self.bulletList,self.allSprites,self.catList,self.poppy_shot,self.sesame_shot,self.garlic_shot,self.mini_shot)
				elif i.bagelType == "flagel" and self.gameOver == False:
					i.erosion(self.catList,self.allSprites,self.explosionList,self.flagel_puff1,self.flagel_puff2,self.extinction)

				i.animate(paused,self.bagel_blink,self.wheat_blink,self.plain_bagel,self.wheat_bagel,self.poppy_bagel,self.poppy_bagel_blink,self.poppy_bagel_shooting,self.poppy_bagel_shooting_blink,self.sesame_bagel,self.sesame_bagel_blink,self.wizard_bagel1,self.wizard_bagel1_blink,self.wizard_bagel2,self.wizard_bagel2_blink,self.wizard_bagel3,self.wizard_bagel3_blink,self.cow_bagel,self.cow_bagel_blink,self.everything_bagel,self.everything_bagel_blink,self.everything_bagel_shooting,self.everything_bagel_shooting_blink,self.crais_bagel,self.crais_bagel_blink,self.multigrain,self.multigrain_blink,self.multigrain_angry,self.multigrain_angry_blink,self.flagel,self.flagel_blink,self.mini_bagels_blink)
				i.spawnWheat(self.wheat_stretch,self.wheat_bagel,self.wheat,self.wheatList,self.allSprites)

				if i.bagelType == "cow" and self.gameOver == False:
					if i.milkLeft <= 0:
						if i.zzzAlpha > 0:
							i.cow_zzz.set_alpha(i.zzzAlpha)
							screen.blit(i.cow_zzz,(i.rect.x + 125, i.rect.y - i.zzzHeight))
							i.zzzHeight += 1
							i.zzzAlpha -= 3
						else:
							i.zzzHeight = 10
							i.zzzAlpha = 255

				elif i.bagelType == "mini": # No gameOver == False
					i.fire(self.poppy_shot,self.bulletList,self.allSprites,self.catList,self.poppy_shot,self.sesame_shot,self.garlic_shot,self.mini_shot)
					for k, v in i.group.iteritems():
						if k == "m1" and v[2] == True:
							v[1] -= 1
							if 0 < v[1] <= 10:
								screen.blit(self.mini_bagels_blink,(i.rect.x + 11,i.rect.y + 6))
							elif v[1] <= 0:
								v[1] = random.randrange(50,350)

							if i.fired == True and paused == False and self.gameOver == False:
								v[0] += i.fireSpeed
								if v[0] >= 140:
									bullet1 = Bullet(i.rect.x + 12, i.rect.y + 11, self.mini_shot, "mini", 0.5, 0, False)
									bullet1.add(self.bulletList)
									bullet1.add(self.allSprites)
									bullet1.bulletHeight = 34
									v[0] = 0
						elif k == "m2" and v[2] == True:
							v[1] -= 1
							if 0 < v[1] <= 10:
								screen.blit(self.mini_bagels_blink,(i.rect.x + 17,i.rect.y + 34))
							elif v[1] <= 0:
								v[1] = random.randrange(50,350)
							if i.fired == True and paused == False and self.gameOver == False:
								v[0] += i.fireSpeed
								if v[0] >= 140:
									bullet2 = Bullet(i.rect.x + 19, i.rect.y + 39, self.mini_shot, "mini", 0.5, 0, False)
									bullet2.add(self.bulletList)
									bullet2.add(self.allSprites)
									bullet2.bulletHeight = 14
									v[0] = 0
						elif k == "m3" and v[2] == True:
							v[1] -= 1
							if 0 < v[1] <= 10:
								screen.blit(self.mini_bagels_blink,(i.rect.x + 46,i.rect.y + 18))
							elif v[1] <= 0:
								v[1] = random.randrange(50,350)
							if i.fired == True and paused == False and self.gameOver == False:
								v[0] += i.fireSpeed
								if v[0] >= 140:
									bullet3 = Bullet(i.rect.x + 47, i.rect.y + 23, self.mini_shot, "mini", 0.5, 0, False)
									bullet3.add(self.bulletList)
									bullet3.add(self.allSprites)
									bullet3.bulletHeight = 24
									v[0] = 0
						if 60 < i.health <= 120:
							i.image = self.mini_bagels1d
							i.mask = pygame.mask.from_surface(i.image)
							#i.rect.x = i.storedx + 3
							#i.rect.y = i.storedy + 9
							if k == "m3":
								v[2] = False
						elif 0 < i.health <= 60:
							i.image = self.mini_bagels2d
							i.mask = pygame.mask.from_surface(i.image)
							#i.rect.x = i.storedx + 3
							#i.rect.y = i.storedy + 9
							if k == "m2":
								v[2] = False

		for i in self.catList:
			if i.catType == "cat" or i.catType == "baby_cat" or i.catType == "ninja_cat" or i.catType == "fondue_cat":
				i.eatEmCat(self.bagelList,self.emptyBList)
			elif i.catType == "taco_cat":
				i.eatEmTacoCat(self.bagelList,self.emptyBList,self.ghostBagelList,self.allSprites,self.plain_bagel,self.poppy_bagel,self.wizard_bagel1,self.wizard_bagel2,self.wizard_bagel3,self.everything_bagel,self.crais_bagel,self.mini_bagels2d)
			if i.catType == "melon_cat":
				i.eatEmCat(self.bagelList,self.emptyBList)
				i.melonFire(self.bagelList,self.melon_cat_shot,self.catBulletList,self.allSprites)
				if 200 > i.fireTimer >= 150 and i.eat == False:
					i.image = self.melon_cat_throw1
					screen.blit(self.special_melon,(i.rect.x - 12,i.rect.y + 12))
				elif 1 <= i.afterShot <= 50 and i.eat == False:
					i.image = self.melon_cat_throw2
			if i.catType == "weenie_cat":
				i.eatEmCat(self.bagelList,self.emptyBList)
				i.spawnBabies(self.baby_cat,self.baby_cat_eating,self.allSprites,self.catList)
			if i.catType == "pizza_cat":
				i.eatEmCat(self.bagelList,self.emptyBList)
				i.rainPizzas(self.pizza,self.allSprites,self.ghostBagelList,self.pizza_cat_ns,self.pizza_cat_eating_ns)
			i.onDeath(self.wheat,self.wheatList,self.allSprites)
			if i.targeted == True:
				pygame.draw.rect(screen,(232,221,29),(i.rect.x + 15, i.rect.y + 50,40,5))

		for i in self.ninja_cat_rope_list: # Ninja cat's gotta be here for obvious reasons
			screen.blit(self.ninja_cat_rope,(i[0],i[1]))
			if paused == False:
				i[1] += 5
			if i[1] + 430 >= i[2]:
				cat = Cat("ninja_cat",10,i[0],i[2],self.ninja_cat,self.ninja_cat_eating,self.catNumber)
				cat.storedY = i[2]
				cat.add(self.catList)
				cat.add(self.bagelCatList)
				cat.add(self.allSprites)
				self.rope_list.append([i[0],i[1]])
				self.ninja_cat_rope_list.remove(i)
				
		for i in self.rope_list: # This probably doesn't have to be here but hey what else does
			screen.blit(self.rope,(i[0],i[1]))
			if paused == False:
				i[1] -= 3
			if i[1] + 480 <= 0:
				self.rope_list.remove(i)

		for i in self.wheatMoveList:
			if paused == False: 
				i[2] += -(i[0]) # See eventProcess
				i[3] += -(i[1])
				screen.blit(self.wheat,(i[2],i[3]))
				wheatCollision = pygame.Rect(i[2],i[3],50,50)
				if self.wheatmilk_box.colliderect(wheatCollision):
					self.wheatMoveList.remove(i)
					self.lightBox = 5

		self.wheatList.draw(screen)

		# And above all else...
		if 0 < self.displayWave <= 200 and not self.titleOn and (paused == False and self.gameOver == False):
			wave_count = self.wave_font.render("Wave " + str(self.wave),False,(0,0,0))
			if self.wave < 10:
				grayRect = pygame.Surface((132,40)) #140
			else:
				grayRect = pygame.Surface((150,40)) #140
			grayRect.set_alpha(200)
			grayRect.fill((120,120,120))
			screen.blit(grayRect,(332,195))
			screen.blit(wave_count,(340,200))
			self.displayWave -= 1

		for i in self.ghostBagelList:
			i.rot_center()


	def drawHand(self):
		global particle_list
		# Cow Bagel Garbage
		bagelInFront = False
		catInFront = False
		goAhead = False
		explodeFill = pygame.Surface((800,480))
		if self.clicked == True:
			pos = pygame.mouse.get_pos()
			for i in self.emptyBList:
				if i.rect.collidepoint(pos[0],pos[1]) and not pygame.sprite.spritecollide(i, self.emptyCowBList, False) and not pygame.sprite.spritecollide(i, self.catList, False) and not pygame.sprite.spritecollide(i, self.trailList, False) and paused == False:
					#print("swell")
					#print(i.id)
					particle_list = self.create_particles(particle_list, (i.rect.x + 33, i.rect.y + 33), (117,66,0), 40, 25, None)
					if android:
						android.vibrate(0.05)
					if self.hasBagel == "plain":
						i.reInit("plain",self.plain_bagel,180)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.plainRecharge = True
						self.wheatCount -= self.plainCost
						if self.particleSetting == False:
							self.bagelPlace.play()
					elif self.hasBagel == "wheat":
						i.reInit("wheat",self.wheat_bagel,180)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.wheatRecharge = True
						self.wheatCount -= self.wheatCost
						if self.particleSetting == False:
							self.bagelPlace.play()
					elif self.hasBagel == "poppy":
						i.reInit("poppy",self.poppy_bagel,180)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.poppyRecharge = True
						self.wheatCount -= self.poppyCost
						if self.particleSetting == False:
							self.bagelPlace.play()
					elif self.hasBagel == "sesame":
						i.reInit("sesame",self.sesame_bagel,1500) # 840 x24
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.sesameRecharge = True
						self.wheatCount -= self.sesameCost
						if self.particleSetting == False:
							self.bagelPlace.play()
					elif self.hasBagel == "wizard":
						i.reInit("wizard",self.wizard_bagel1,60)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.wizardRecharge = True
						self.wheatCount -= self.wizardCost
						if self.particleSetting == False:
							self.bagelPlace.play()
					elif self.hasBagel == "cow":
						if len(self.bagelList) != 0:
							for k in self.bagelList:
								if k.bagelType == "cow":
									if k.rect.collidepoint(i.rect.x - 66,i.rect.y + 20):
										bagelInFront = True
								else:
									if k.rect.collidepoint(i.rect.x,i.rect.y + 20):
										bagelInFront = True

						if len(self.catList) != 0:
							for x in self.catList:
								if x.rect.collidepoint(i.rect.x - 66,i.rect.y + 20):
									catInFront = True

						if bagelInFront == False and catInFront == False:
							i.reInit("cow",self.cow_bagel,660)
							i.add(self.bagelList)
							i.remove(self.emptyBList)
							emptyB = emptyBagel(i.rect.x, i.rect.y, self.empty_tile)
							emptyB.add(self.emptyCowBList)
							i.emptyBagel = emptyB
							self.cowRecharge = True
							self.wheatCount -= self.cowCost
							if self.particleSetting == False:
								self.bagelPlace.play()

					elif self.hasBagel == "everything":
						i.reInit("everything",self.everything_bagel,180)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.everyRecharge = True
						self.wheatCount -= self.everyCost
						if self.particleSetting == False:
							self.bagelPlace.play()

					elif self.hasBagel == "crais":
						i.reInit("crais",self.crais_bagel,180)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.craisRecharge = True
						self.wheatCount -= self.craisCost
						if self.particleSetting == False:
							self.bagelPlace.play()

					elif self.hasBagel == "multi":
						i.reInit("multi",self.multigrain,600)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.multiRecharge = True
						self.wheatCount -= self.multiCost
						if self.particleSetting == False:
							self.bagelPlace.play()

					elif self.hasBagel == "flagel":
						i.reInit("flagel",self.flagel,1)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.flagelRecharge = True
						self.wheatCount -= self.flagelCost
						if self.particleSetting == False:
							self.bagelPlace.play()

					elif self.hasBagel == "mini":
						i.reInit("mini",self.mini_bagels,180)
						i.add(self.bagelList)
						i.remove(self.emptyBList)
						self.miniRecharge = True
						self.wheatCount -= self.miniCost
						if self.particleSetting == False:
							self.bagelPlace.play()

					self.hasBagel = "null"
					self.clicked = False

		#print(self.selecting)
		if self.clicked == False and self.selecting == True:
			pos = pygame.mouse.get_pos()
			for i in self.emptyBList:
				if i.rect.collidepoint(pos[0],pos[1]) and paused == False:
					#print(i.id)
					if self.selecting == True:
						i.bagelSelected = True
				elif not i.rect.collidepoint(pos[0],pos[1]):
					i.bagelSelected = False

			for i in self.bagelList:
				tempRect = pygame.Rect(i.storedx,i.storedy,66,66)
				if tempRect.collidepoint(pos[0],pos[1]) and paused == False:
					#print("naisu")
					if self.selecting == True:
						i.bagelSelected = True
				elif not tempRect.collidepoint(pos[0],pos[1]):
					i.bagelSelected = False


		if self.extinction[0] > 0 and paused == False: # When you have no other place to put this
			if self.extinction[0] == 255:
				self.flagelCapacity = 1600
				self.flagelRechargeTime = 0
			explodeFill.set_alpha(self.extinction[0])
			explodeFill.fill((255,255,255))
			screen.blit(explodeFill,(0,0))
			self.extinction[0] -= 1

	#def drawCC(self):


	def spawnCats(self):
		"""self.spawnTime += 1
		self.waveTime += 1
		for i in range(self.numOfCats):
			if self.spawnTime >= (random.randrange(600,800)):
				self.spawnTime = 0

				
		if self.waveTime >= 6000:
			self.wave += 1
			self.levelInc += 50
			self.waveTime = 0
			self.numOfCats += 1
			print(self.wave)"""

		spawnValue = 0

		if self.preGame == True and (paused == False and self.gameOver == False):
			self.preGameTime += 1
			if self.preGameTime >= 1: #900?
				self.preGame = False
				for i in range(self.instances):
					spawnValue = random.randint(0,900)
					self.preCatList.append(spawnValue)

		if self.preGame == False and (paused == False and self.gameOver == False):
			self.spawnTime += 1
			self.waveTime += 1
			for i in self.preCatList:
				if i == self.spawnTime:
					catType = random.choice(self.catTypes)
					if catType == "cat":
						position = random.randrange(11,394,66)
						cat = Cat("cat",10,1100,position,self.cat,self.cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.storedY = position
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
					elif catType == "taco_cat":
						position = random.randrange(11,394,66)
						cat = Cat("taco_cat",20,1100,position,self.taco_cat,self.taco_cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.storedY = position
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
					elif catType == "melon_cat":
						position = random.randrange(11,394,66)
						cat = Cat("melon_cat",30,1100,position,self.melon_cat,self.melon_cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.storedY = position
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
					elif catType == "weenie_cat":
						position = random.randrange(11,394,66)
						cat = Cat("weenie_cat",30,1100,position,self.weenie_cat,self.weenie_cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.storedY = position
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
					elif catType == "baby_cat":
						position = random.randrange(11,394,66)
						cat = Cat("baby_cat",2,1100,position + 13,self.baby_cat,self.baby_cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.storedY = position
						cat.speed = 3
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
					elif catType == "ninja_cat":
						position = random.randrange(11,394,66)
						self.ninja_cat_rope_list.append([random.randrange(425,755),-480,position])
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
					elif catType == "pizza_cat":
						position = random.randrange(11,394,66)
						cat = Cat("pizza_cat",10,1100,position - 7,self.pizza_cat,self.pizza_cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.shield = 40
						cat.totalShield = 40
						cat.storedY = position
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
					elif catType == "fondue_cat":
						position = random.randrange(11,394,66)
						cat = Cat("fondue_cat",20,1100,position,self.fondue_cat,self.fondue_cat_eating,self.catNumber)
						if self.exclaim == True:
							self.drawDanger = position
							self.exclaim = False
						cat.storedY = position
						cat.add(self.catList)
						cat.add(self.bagelCatList)
						cat.add(self.allSprites)
						# Specific to fondue cat
						trail = Trail(1100,position,self.catNumber,cat)
						trail.add(self.trailList)
						trail.add(self.allSprites)
					self.catNumber += 1
				if self.spawnTime >= 900:
					self.spawnTime = 0
					del self.preCatList[:]
					for i in range(self.instances):
						spawnValue = random.randint(0,900)
						self.preCatList.append(spawnValue)
			if self.waveTime >= 3600:
				self.instances += 1
				self.waveTime = 0
				self.wave += 1
				self.displayWave = 200
				if self.wave >= 2:
					self.catTypes.append("cat")
					self.catTypes.append("cat")
					self.catTypes.append("taco_cat")
				if self.wave >= 3:
					self.catTypes.append("ninja_cat")
					self.catTypes.append("baby_cat")
				if self.wave >= 4:
					self.catTypes.append("taco_cat")
					self.catTypes.append("fondue_cat")
					self.catTypes.append("fondue_cat")
					self.catTypes.append("melon_cat")
					self.catTypes.append("melon_cat")
				if self.wave >= 5:
					self.catTypes.append("weenie_cat")
					self.catTypes.append("weenie_cat")
					self.catTypes.append("melon_cat")
					self.catTypes.append("fondue_cat")
					self.catTypes.append("ninja_cat")
				if self.wave >= 7:
					self.catTypes.append("pizza_cat")
					self.catTypes.append("fondue_cat")
				if self.wave >= 8:
					self.catTypes.append("pizza_cat")
					self.catTypes.append("pizza_cat")
					self.catTypes.append("fondue_cat")
				if self.wave >= 10:
					self.catTypes.append("pizza_cat")
					self.catTypes.append("pizza_cat")
					self.catTypes.append("pizza_cat")
					self.catTypes.append("fondue_cat")

	def spawnBagels(self):
		global particle_list
		bagelID = 0
		for row in range(6):
			for column in range(12):
				bagel = Bagel((column*66),(row*66))
				bagel.id = bagelID
				bagelID += 1
				bagel.add(self.emptyBList)
				bagel.add(self.allSprites)

	def spawnOffTitle(self):
		if self.titleOn == False:
			return False
		elif self.titleOn == True:
			return True

	def projectileCollision(self):
		global particle_list
		for i in self.bulletList:
			if pygame.sprite.spritecollide(i, self.catList, False) and i.bulletType and paused == False:
				for k in self.catList:
					if pygame.sprite.collide_mask(k, i):
						if i.bulletType == "bagel":
							if k.shield > 0:
								k.shield -= i.damage
							else:
								k.health -= i.damage

							if self.particleSetting == False:
								self.bagelSplat.play()
							i.kill()
							i.remove()
							if k.catType == "pizza_cat" and k.shield > 0:
								i.remove(self.bulletList)
								i.add(self.catBulletList)
								i.bulletCatType = "bagel"
								i.speed = -7
							else:
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y), (229,218,165), 15, 33, None)
						elif i.bulletType == "poppy":
							if k not in i.hitList:
								if k.shield > 0:
									k.shield -= i.damage
								else:
									k.health -= i.damage
								k.add(i.hitList)
								if k.catType == "pizza_cat" and k.shield > 0:
									i.remove(self.bulletList)
									i.add(self.catBulletList)
									i.bulletCatType = "poppy"
									i.speed = -7
								else:
									particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y), (187,187,187), 2, 33, None)
						elif i.bulletType == "wizard":
							if k.shield > 0:
								k.shield -= i.damage
							else:
								k.health -= i.damage
							if i.level >= 2 and k.caged == False:
								k.rect.x += 50
								k.move = True
								k.eat = False
								k.victim = None
							if self.particleSetting == False:
								self.wizardSplat.play()
							i.kill()
							i.remove()
							if k.catType == "pizza_cat" and k.shield > 0:
									i.remove(self.bulletList)
									i.add(self.catBulletList)
									i.image = self.wizard_shot_r
									i.bulletCatType = "wizard"
									i.speed = -7
							else:
								particle_list = self.create_particles(particle_list, (k.rect.x - 12,k.rect.y + 15), (255,39,1), 5, 33, None)	
						elif i.bulletType == "garlic":
							if self.particleSetting == False:
								self.bagelSplat.play()
							k.garlicStacks += 1
							i.kill()
							i.remove()
							if k.catType == "pizza_cat" and k.shield > 0:
									i.remove(self.bulletList)
									i.add(self.catBulletList)
									i.bulletCatType = "garlic"
									i.speed = -7
							else:
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y), (232,226,197), 15, 33, None)
						elif i.bulletType == "sesame":
							if self.particleSetting == False:
								self.bagelSplat.play()
							if k.shield > 0:
								k.shield -= i.damage
							else:
								k.health -= i.damage
							i.kill()
							i.remove()
							if k.catType == "pizza_cat" and k.shield > 0:
									i.remove(self.bulletList)
									i.add(self.catBulletList)
									i.bulletCatType = "sesame"
									i.speed = -7
							else:
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y), (217,188,108), 15, 33, None)
						elif i.bulletType == "melon_r":
							particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (221,54,37), 10, 33, None) # One for the melon
							particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (78,181,75), 10, 33, None) # Two for the rind
							if self.particleSetting == False:
								self.bagelSplat.play()
							if k.shield > 0:
								k.shield -= i.damage
							else:
								k.health -= i.damage
							i.kill()
							i.remove()
						elif i.bulletType == "melon_r_thru":
							if k not in i.hitList:
								if k.shield > 0:
									k.shield -= i.damage
								else:
									k.health -= i.damage
								k.add(i.hitList)
								if self.particleSetting == False:
									self.bagelSplat.play()
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (221,54,37), 10, 33, None)
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (78,181,75), 10, 33, None)
						elif i.bulletType == "mini":
							if k.shield > 0:
								k.shield -= i.damage
							else:
								k.health -= i.damage

							if self.particleSetting == False:
								pass
								#self.bagelSplat.play()
							i.kill()
							i.remove()
							particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y), (229,218,165), 1, i.bulletHeight, None)

					
	def catProjectileCollision(self):
		global particle_list
		for i in self.catBulletList:
			if pygame.sprite.spritecollide(i, self.bagelList, False) and paused == False:
				for k in self.bagelList:
					if pygame.sprite.collide_mask(k, i) and k.bagelType != "flagel": # Ignore melons and pizza cat shots
						if k.blockChance != 2 and i.bulletCatType == "melon":
							particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (221,54,37), 10, 33, None)
							particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (78,181,75), 10, 33, None)
							if k.immune == False:
								k.health -= 60
							i.kill()
							i.remove()
							if k.bagelType == "multi":
								k.blockChance = random.choice([1,2])
						elif k.blockChance == 2 and i.bulletCatType == "melon":
							if k.fired == False and k.holdMelon == False:
								k.holdMelon = True
								i.kill()
								i.remove()
								k.blockChance = random.choice([1,2])
							elif k.fired == True or k.holdMelon == False:
								if i.bulletCatType == "melon":
									particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (221,54,37), 10, 33, None)
									particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (78,181,75), 10, 33, None)
									if k.immune == False:
										k.health -= 60
								
						elif i.bulletCatType != "melon":
							if i.bulletCatType == "bagel":
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (229,218,165), 10, 33, None)
								if k.immune == False:
									k.health -= 10
							elif i.bulletCatType == "poppy":
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (128,128,128), 10, 33, None)
								if k.immune == False:
									k.health -= 10
							elif i.bulletCatType == "sesame":
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (217,188,108), 10, 33, None)
								if k.immune == False:
									k.health -= 10
							elif i.bulletCatType == "garlic":
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y + 5), (232,226,197), 10, 33, None)
								if k.immune == False:
									k.health -= 10
							elif i.bulletCatType == "wizard":
								particle_list = self.create_particles(particle_list, (i.rect.x,i.rect.y - 8), (255,39,1), 10, 33, None)
								if k.immune == False:
									k.health -= 15
							i.remove()
							i.kill()

			
	def eatBagels(self):
		for i in self.bagelList:
			if pygame.sprite.spritecollide(i, self.catList, False, pygame.sprite.collide_mask) and paused == False:
				for k in self.catList:
					if pygame.sprite.collide_mask(k, i):
						if i.bagelType != "flagel": # Ignore walking on flagels
							k.victim = i

		# Dog eating is also here too
		for k in self.catList:
			if pygame.sprite.spritecollide(k, self.dogList, False, pygame.sprite.collide_mask) and paused == False:
				for j in self.dogList:
					if pygame.sprite.collide_mask(j, k):
						j.victim = k

		# And cats eating dogs
		for q in self.dogList:
			if pygame.sprite.spritecollide(q, self.catList, False, pygame.sprite.collide_mask) and paused == False:
				for w in self.catList:
					if pygame.sprite.collide_mask(w, q):
						w.victim = q


	def cageCats(self):
		global particle_list
		for i in self.cageList:
			if pygame.sprite.spritecollide(i, self.catList, False, pygame.sprite.collide_mask) and paused == False:
				for k in self.catList:
					if pygame.sprite.collide_mask(k, i):
						if k not in i.hitList:
							if i.stopped == False:
								k.add(i.hitList)
								if k.shield > 0:
									k.shield -= 6
								else:
									k.health -= 6
						if i.stopped == True:
							if i.disTimer == 2:
								if i.victim == None and k.caged == False: # and k.targeted == True
									i.victim = k
									i.victim.move = False
									i.victim.eat = False
									if i.victim.shield > 0:
										i.victim.shield -= 2
									else:
										i.victim.health -= 2
									i.victim.caged = True
									if k.catType == "pizza_cat":
										i.rect.x = i.victim.rect.x - 5
									else:
										i.rect.x = i.victim.rect.x - 15

	def explosionCollision(self):
		global particle_list
		for i in self.explosionList:
			if i.formParticles == True:
				particle_list = self.create_particles(particle_list, (i.rect.x + 99,i.rect.y + 104), (229,218,165), 120, -33, "high")
				particle_list = self.create_particles(particle_list, (i.rect.x + 99,i.rect.y + 104), (229,218,165), 120, 33, None)
				particle_list = self.create_particles(particle_list, (i.rect.x + 99,i.rect.y + 104), (229,218,165), 120, 99, None)
			if pygame.sprite.spritecollide(i, self.catList, False, pygame.sprite.collide_rect) and paused == False:
				for k in self.catList:
					if pygame.sprite.collide_rect(k, i):
						if k.shield > 0:
							k.shield = 0
						else:
							k.health -= 20
						i.remove()
						i.kill()

		# Throwin' in the cat speed up from fondue
		for q in self.catList:
			if pygame.sprite.spritecollide(q, self.trailList, False) and q.catType != "fondue_cat" and paused == False:
				for w in self.trailList:
					if pygame.sprite.collide_rect(w, q):
						if q.catType != "baby_cat" and q.catType != "fondue_cat":
							q.speed = 2

			if not pygame.sprite.spritecollide(q, self.trailList, False) and q.catType != "fondue_cat" and paused == False:
				if q.catType != "baby_cat" and q.catType != "fondue_cat":
					q.speed = q.storedSpeed

	def createHealthBars(self):
		for i in self.catList:
			healthPercent = i.health / i.totalHealth
			health = round(40 * healthPercent)
			# Not every cat has a shield
			# Not every integer can be divided by 0
			if i.shield != None:
				shieldPercent = i.shield / i.totalShield
				shield = round(40 * shieldPercent)
			# Not every teacher is as good as Gino
			#BringGinoToIB
			if i.catType == "cat" or i.catType == "taco_cat" or i.catType == "melon_cat" or i.catType == "ninja_cat" or i.catType == "fondue_cat":
				pygame.draw.rect(screen,(255,0,0),(i.rect.x + 73,i.rect.y + 46,3,-40))
				pygame.draw.rect(screen,(0,0,255),(i.rect.x + 73,i.rect.y + 46,3, -health))
			elif i.catType == "weenie_cat":
				pygame.draw.rect(screen,(255,0,0),(i.rect.x + 111,i.rect.y + 46,3,-40))
				pygame.draw.rect(screen,(0,0,255),(i.rect.x + 111,i.rect.y + 46,3, -health))
			elif i.catType == "baby_cat":
				pygame.draw.rect(screen,(255,0,0),(i.rect.x + 46,i.rect.y + 23,3,-40 / 2))
				pygame.draw.rect(screen,(0,0,255),(i.rect.x + 46,i.rect.y + 23,3, -health / 2))
			elif i.catType == "pizza_cat" and i.pizzaDown == False:
				pygame.draw.rect(screen,(255,0,0),(i.rect.x + 84,i.rect.y + 49,3,-40))
				pygame.draw.rect(screen,(0,0,255),(i.rect.x + 84,i.rect.y + 49,3, -health))
				pygame.draw.rect(screen,(77,77,77),(i.rect.x + 84,i.rect.y + 49,3, -shield))
			elif i.catType == "pizza_cat" and i.pizzaDown == True:
				pygame.draw.rect(screen,(255,0,0),(i.rect.x + 73,i.rect.y + 49,3,-40))
				pygame.draw.rect(screen,(0,0,255),(i.rect.x + 73,i.rect.y + 49,3, -health))
				pygame.draw.rect(screen,(77,77,77),(i.rect.x + 73,i.rect.y + 49,3, -shield))

		for i in self.bagelList:
			if i.bagelType != "flagel":
				healthPercent = i.health / i.totalHealth
				health = round(30 * healthPercent)
				pygame.draw.rect(screen,(255,0,0),(i.storedx + 18,i.storedy + 66,30,3))
				pygame.draw.rect(screen,(0,0,255),(i.storedx + 18,i.storedy + 66,health,3))

		for k in self.dogList:
			healthPercent = k.health / k.totalHealth
			health = round(30 * healthPercent)
			pygame.draw.rect(screen,(255,0,0),(k.rect.x - 12,k.rect.y + 43,3,-40))
			pygame.draw.rect(screen,(0,0,255),(k.rect.x - 12,k.rect.y + 43,3,-health))


	def pause(self):
		global paused
		#legit the shortest function in the universe
		if paused == True:
			screen.blit(self.pause_menu,(0,0))
			if self.options == True:
				screen.blit(self.options_menu,(0,0))
				screen.blit(self.music_slider,(296 + self.music_slider_value,173))
				screen.blit(self.sound_slider,(296 + self.sound_slider_value,218))
				if self.musicOff:
					screen.blit(self.grayed_out_music,(361,74))
				if self.soundOff:
					screen.blit(self.grayed_out_sound,(450,74))
				if self.particleSetting:
					screen.blit(self.grayed_out_particles_button,(493,271))
			elif self.info == True:
				screen.blit(self.info_screen,(0,0))
		elif self.gameOver == True:
			screen.blit(self.game_over_screen,(0,0))

		if android and self.titleOn == False:
			if android.check_pause():
				android.wait_for_resume()
				paused = True


	def restartGame(self):
		global paused, particle_list
		self.bagelList.empty()
		self.catList.empty()
		self.wheatList.empty()
		self.bulletList.empty()
		self.catBulletList.empty()
		self.emptyBList.empty()
		self.emptyCowBList.empty()
		self.catBulletList.empty()
		self.cageList.empty()
		self.dogList.empty()
		self.trailList.empty()
		particle_list = []
		self.allSprites.empty()
		self.bagelCatList.empty()
		self.cageList.empty()
		self.rope_list = []
		self.ninja_cat_rope_list = []
		self.page = 1
		self.hasBagel = "null"
		self.plainRecharge = False
		self.wheatRecharge = False
		self.poppyRecharge = False
		self.sesameRecharge = False
		self.wizardRecharge = False
		self.cowRecharge = False
		self.everyRecharge = False
		self.craisRecharge = False
		self.multiRecharge = False
		self.flagelRecharge = False
		self.flagelCapacity = 900 # for the sake of completeness
		self.plainRechargeTime = 0
		self.wheatRechargeTime = 0
		self.poppyRechargeTime = 0
		self.sesameRechargeTime = 0
		self.wizardRechargeTime = 0
		self.cowRechargeTime = 0
		self.everyRechargeTime = 0
		self.craisRechargeTime = 0
		self.multiRechargeTime = 0
		self.flagelRechargeTime = 0
		self.preGame = True
		self.preGameTime = 0
		self.spawnTime = 0
		self.waveTime = 0
		self.wave = 1
		self.displayWave = 200
		self.preCatList = []
		self.instances = 1
		self.catTypes = ["cat","cat","cat","cat","cat","cat"]
		self.exclaim = True
		self.drawDanger = 0
		self.dangerTimer = 0
		self.dangerAlpha = 2
		self.dangerTurn = 0
		self.wavePercentRaw = 0
		self.wavePercent = 0
		self.waveBar = 0
		self.wheatCount = 5
		self.milk = 0
		self.extinction = [0]
		self.restart = False
		paused = False
		self.spawnBagels()

	def rechargeBagels(self):
		"""for i in self.catList:
			print(i.__dict__) # important but not now
		"""
		if paused == False:
			if self.plainRecharge == True:
				self.plainRechargeTime += 1
				if self.plainRechargeTime >= self.plainCapacity:
					self.plainRecharge = False
					self.plainRechargeTime = 0
			if self.wheatRecharge == True:
				self.wheatRechargeTime += 1
				if self.wheatRechargeTime >= self.wheatCapacity:
					self.wheatRecharge = False
					self.wheatRechargeTime = 0
			if self.poppyRecharge == True:
				self.poppyRechargeTime += 1
				if self.poppyRechargeTime >= self.poppyCapacity:
					self.poppyRecharge = False
					self.poppyRechargeTime = 0
			if self.sesameRecharge == True:
				self.sesameRechargeTime += 1
				if self.sesameRechargeTime >= self.sesameCapacity:
					self.sesameRecharge = False
					self.sesameRechargeTime = 0
			if self.wizardRecharge == True:
				self.wizardRechargeTime += 1
				if self.wizardRechargeTime >= self.wizardCapacity:
					self.wizardRecharge = False
					self.wizardRechargeTime = 0
			if self.cowRecharge == True:
				self.cowRechargeTime += 1
				if self.cowRechargeTime >= self.cowCapacity:
					self.cowRecharge = False
					self.cowRechargeTime = 0
			if self.everyRecharge == True:
				self.everyRechargeTime += 1
				if self.everyRechargeTime >= self.everyCapacity:
					self.everyRecharge = False
					self.everyRechargeTime = 0
			if self.craisRecharge == True:
				self.craisRechargeTime += 1
				if self.craisRechargeTime >= self.craisCapacity:
					self.craisRecharge = False
					self.craisRechargeTime = 0
			if self.multiRecharge == True:
				self.multiRechargeTime += 1
				if self.multiRechargeTime >= self.multiCapacity:
					self.multiRecharge = False
					self.multiRechargeTime = 0
			if self.flagelRecharge == True:
				self.flagelRechargeTime += 1
				if self.flagelRechargeTime >= self.flagelCapacity:
					self.flagelRecharge = False
					self.flagelRechargeTime = 0
					self.flagelCapacity = 900 # Specific to flagels, after extinction
			if self.miniRecharge == True:
				self.miniRechargeTime += 1
				if self.miniRechargeTime >= self.miniCapacity:
					self.miniRecharge = False
					self.miniRechargeTime = 0

	def musicTracks(self):
		music_volume = 0.03 * (self.music_slider_value / 184) # 0.08
		if self.musicOff:
			mixer.music.set_volume(0)
		else:
			mixer.music.set_volume(music_volume)

		if self.soundOff:
			for i in self.soundList:
				i.set_volume(0)
		else:
			bagelSplat_vol = 0.05 * (self.sound_slider_value / 184) 
			poppySplat_vol = 0.5 * (self.sound_slider_value / 184)
			wizardSplat_vol = 0.075 * (self.sound_slider_value / 184)
			cageDrop_vol = 0.3 * (self.sound_slider_value / 184)
			punch_vol = 0.3 * (self.sound_slider_value / 184)
			self.bagelSplat.set_volume(bagelSplat_vol)
			self.poppySplat.set_volume(poppySplat_vol)
			self.wizardSplat.set_volume(wizardSplat_vol)
			self.cageDrop.set_volume(cageDrop_vol)
			self.punch.set_volume(punch_vol)
			self.fork.set_volume(punch_vol)
		if self.titleOn == False:
			if self.firstRun == True:
				mixer.music.load("track1.ogg")
				mixer.music.play(-1)
				mixer.music.set_volume(music_volume)
				self.firstRun = False
		else:
			if self.titleRun == True:
				mixer.music.play(-1)
				mixer.music.set_volume(0.02)
				self.titleRun = False
		
	def saveGame(self):
		global particle_list
		with open('save.dat','wb') as f:
			#pickle.dump(particle_list,f)
			pickle.dump(self.page,f)
			pickle.dump(self.hasBagel,f)
			pickle.dump(self.plainRecharge,f)
			pickle.dump(self.wheatRecharge,f)
			pickle.dump(self.poppyRecharge,f)
			pickle.dump(self.sesameRecharge,f)
			pickle.dump(self.wizardRecharge,f)
			pickle.dump(self.cowRecharge,f)
			pickle.dump(self.everyRecharge,f)
			pickle.dump(self.craisRecharge,f)
			pickle.dump(self.multiRecharge,f)
			pickle.dump(self.flagelRecharge,f)
			pickle.dump(self.plainRechargeTime,f)
			pickle.dump(self.wheatRechargeTime,f)
			pickle.dump(self.poppyRechargeTime,f)
			pickle.dump(self.sesameRechargeTime,f)
			pickle.dump(self.wizardRechargeTime,f)
			pickle.dump(self.cowRechargeTime,f)
			pickle.dump(self.everyRechargeTime,f)
			pickle.dump(self.craisRechargeTime,f)
			pickle.dump(self.multiRechargeTime,f)
			pickle.dump(self.flagelRechargeTime,f)
			pickle.dump(self.preGame,f)
			pickle.dump(self.preGameTime,f)
			pickle.dump(self.spawnTime,f)
			pickle.dump(self.waveTime,f)
			pickle.dump(self.wave,f)
			pickle.dump(self.preCatList,f)
			pickle.dump(self.instances,f)
			pickle.dump(self.catTypes,f)
			pickle.dump(self.exclaim,f)
			pickle.dump(self.drawDanger,f)
			pickle.dump(self.dangerTimer,f)
			pickle.dump(self.dangerAlpha,f)
			pickle.dump(self.dangerTurn,f)
			pickle.dump(self.wavePercentRaw,f)
			pickle.dump(self.wavePercent,f)
			pickle.dump(self.waveBar,f)
			pickle.dump(self.wheatCount,f)
			pickle.dump(self.milk,f)
			pickle.dump(self.extinction,f)
			pickle.dump(self.allSprites,f)
		f.close()

	def loadGame(self):
		with open('save.dat', 'rb') as fp:
			self.page = pickle.load(fp)
			self.hasBagel = pickle.load(fp)
			self.plainRecharge = pickle.load(fp)
			self.wheatRecharge = pickle.load(fp)
			self.poppyRecharge = pickle.load(fp)
			self.sesameRecharge = pickle.load(fp)
			self.wizardRecharge = pickle.load(fp)
			self.cowRecharge = pickle.load(fp)
			self.everyRecharge = pickle.load(fp)
			self.craisRecharge = pickle.load(fp)
			self.multiRecharge = pickle.load(fp)
			self.flagelRecharge = pickle.load(fp)
			self.plainRechargeTime = pickle.load(fp)
			self.wheatRechargeTime = pickle.load(fp)
			self.poppyRechargeTime = pickle.load(fp)
			self.sesameRechargeTime = pickle.load(fp)
			self.wizardRechargeTime = pickle.load(fp)
			self.cowRechargeTime = pickle.load(fp)
			self.everyRechargeTime = pickle.load(fp)
			self.craisRechargeTime = pickle.load(fp)
			self.multiRechargeTime = pickle.load(fp)
			self.flagelRechargeTime = pickle.load(fp)
			self.preGame = pickle.load(fp)
			self.preGameTime = pickle.load(fp)
			self.spawnTime = pickle.load(fp)
			self.waveTime = pickle.load(fp)
			self.wave = pickle.load(fp)
			self.preCatList = pickle.load(fp)
			self.instances = pickle.load(fp)
			self.catTypes = pickle.load(fp)
			self.exclaim = pickle.load(fp)
			self.drawDanger = pickle.load(fp)
			self.dangerTimer = pickle.load(fp)
			self.dangerAlpha = pickle.load(fp)
			self.dangerTurn = pickle.load(fp)
			self.wavePercentRaw = pickle.load(fp)
			self.wavePercent = pickle.load(fp)
			self.waveBar = pickle.load(fp)
			self.wheatCount = pickle.load(fp)
			self.extinction = pickle.load(fp)
			self.milk = pickle.load(fp)
			allSprites = pickle.load(fp)
			"""bagelList = pickle.load(fp)
			emptyBList = pickle.load(fp)
			catList = pickle.load(fp)
			bulletList = pickle.load(fp)
			catBulletList = pickle.load(fp)
			wheatList = pickle.load(fp)
			ghostBagelList = pickle.load(fp)
			emptyCowBList = pickle.load(fp)
			cageList = pickle.load(fp)"""

	# Particle Functions
 
	def create_particles(self, p_list, position, color, particle_count, height, p_type):
		if self.particleSetting:
			particle_count = int(round(particle_count * 0.2))
		numbers = range(-5, -1) + range(1, 5)
 
		for i in range(0, particle_count):
			if p_type != "high":
				p = Particle(position[0], position[1], random.choice(numbers), random.choice(numbers), random.randint(1, 5), color, height, p_type)
			else:
				p = Particle(position[0], position[1], random.choice(numbers), random.choice([random.uniform(-7.0,-2.0),random.uniform(4.0,8.0)]), random.randint(1, 5), color, height, p_type)
			p_list.append(p)
 
		return p_list

	def formParticles(self):
		global particle_list
		for i in particle_list:
			i.killEverything(particle_list)
				
		for i in range(0, len(particle_list)):
			particle_list[i].update(paused)
 
		for i in range(0, len(particle_list)):
			particle_list[i].display(screen)

		for x in range(0, len(particle_list)):
			try:
				if not pygame.sprite.collide_rect(screen, particle_list[len(particle_list) - x - 1]):
					del particle_list[len(particle_list) - x - 1]
			except:
				break

	def eatingParticles(self):
		global particle_list
		for i in self.catList:
			if i.victim != None and paused == False and i.eat:
				if i.victim.bagelType == "plain" or i.victim.bagelType == "poppy" or i.victim.bagelType == "sesame" or i.victim.bagelType == "wizard" or i.victim.bagelType == "cow" or i.victim.bagelType == "everything" or i.victim.bagelType == "crais":
					if i.catType == "baby_cat":
						particle_list = self.create_particles(particle_list, (i.rect.x + 18,i.rect.y + 10), (229,218,165), 1, 26, None) # All heights down by 2
					else:
						particle_list = self.create_particles(particle_list, (i.rect.x + 23,i.rect.y + 15), (229,218,165), 1, 32, None)
				elif i.victim.bagelType == "wheat" or i.victim.bagelType == "crais":
					if i.catType == "baby_cat":
						particle_list = self.create_particles(particle_list, (i.rect.x + 18,i.rect.y + 8), (156,111,40), 1, 26, None)
					else:
						particle_list = self.create_particles(particle_list, (i.rect.x + 23,i.rect.y + 15), (156,111,40), 1, 32, None)
				elif i.victim.bagelType == "multi":
					if i.catType == "baby_cat":
						particle_list = self.create_particles(particle_list, (i.rect.x + 18,i.rect.y + 8), (172,102,45), 1, 26, None)
					else:
						particle_list = self.create_particles(particle_list, (i.rect.x + 23,i.rect.y + 15), (172,102,45), 1, 32, None)
				





