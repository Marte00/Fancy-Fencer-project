from menu import *
import pygame as pg
import os
from scene import Scene
from player import Player

print('\n')
print('	Jouer à Fancy Fancer ?\n')
print('Entrez 1 : pour la version terminal\n')
print('Entrez 2 : pour la version graphique\n')


while True:
	
	entrez = input('Choisissez ! : ')
	
	if entrez == '1':
		os.system('clear')
		print_menu()
		break
	elif entrez == '2':
		os.system('clear')
		pg.init()
	
		# création de la fenêtre de jeu
		
		pg.display.set_caption("Fancy Fencing - Duel");
		screen = pg.display.set_mode((1280,800));
		
		
		# lancement du jeu
		
		scene = Scene(screen);
		scene.run();
		
		pg.quit()
		
		break
	else:
		print('Seulement les choix proposés !')
		
