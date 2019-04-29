import pygame
import os
import sys
import random
import webbrowser
from game import *

# Basic Setup
try:
	import android
except ImportError:
	android = None
	
if android:
	android.init()
	android.map_key(android.KEYCODE_BACK, pygame.K_p)

try:
	import pygame.mixer as mixer
except ImportError:
	import android.mixer as mixer

mixer.pre_init(44100, -16, 1, 512)
pygame.init()

clock = pygame.time.Clock()

def main():

	titleOn = True
	spawnSprites = True
	running = True

	game = Game()

	while running:
		titleOn = game.spawnOffTitle()

		running = game.eventProcess()

		if titleOn == False:
			game.spawnCats()
			if spawnSprites == True:
				game.spawnBagels()
				spawnSprites = False

		game.musicTracks()
		
		game.drawBackground()

		game.titleScreen()

		game.eventProcess()

		game.drawSprites()

		game.createHealthBars()

		game.formParticles()

		game.eatingParticles()

		game.drawHand()
		
		game.pause()

		game.eatBagels()

		game.explosionCollision()

		game.cageCats()

		game.projectileCollision()

		game.catProjectileCollision()

		game.rechargeBagels()

		pygame.display.flip()

		clock.tick(45)

	pygame.quit()

if __name__ == "__main__":
	main()