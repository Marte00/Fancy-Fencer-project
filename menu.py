# ce fichier contient le code pour l'interface menu de la version terminal du jeu
# 11-2022
import os
from terminal import *
from termcolor import colored
import pygame as pg

# charge un background
def charge_background(option):
	if option:
		with open("scene1.ffscene") as f:
			line = f.readline()
			l = list(line)
			l = l[:-1]
			return l
			
	else:
		with open("scene2.ffscene") as f:
			line = f.readline()
			l = list(line)
			l = l[:-1]
			return l

# fonction qui retourne le contenu du fichier de sauvegarde version terminal		
def charge_game():
	with open("./game.sav") as f:
		l = []
		for line in f:
			l.append(int(line[:-1]))
		return l

# fonction qui retourne le contenu du fichier de sauvegarde version graphique
def charge_game2():
	with open("./gamegraphique.sav") as f:
		l = []
		for line in f:
			l.append(int(line[:-1]))
		return l

# retourne le background sous forme d'une liste
def change_background(option):
	if option:
		l = charge_background(option)
		x = []
		for i in range(len(l)):
			if l[i] == 'x':
				x.append((i+1)*100//len(l))
		return x
	else:
		l = charge_background(option)
		x = []
		for i in range(len(l)):
			if l[i] == 'x':
				x.append((i+1)*100//len(l))
		return x

# affichage menu principale
def menuP(save):
	os.system('clear')
	print('#---------Bienvenue sur Fancy Fencer---------#\n')
	print('	     MENU PRINCIPAL:\n')
	print(' 1 : Jouer\n')
	print(' 2 : contrôle des joueurs\n')
	if save:
		print(' delete : Supprimer la partie sauvegardée\n')
	else:
		print(colored(' delete : Pas de partie sauvegardée\n', 'grey'))
	print(' 0 : Quittez le jeu\n')

# affichage option Jouer
def option1():
	os.system('clear')
	print('          Choisissez un terrain de combat: \n')
	print(' B1 : BACKGROUND 1\n')
	print(' B2 : BACKGROUND 2\n')
	print(' 3  : Retour\n')
	
	
# affichage option controle
def option2():
	os.system('clear')
	print('          COMMANDE CLAVIER:\n')
	print(' N : Mettre en pause \n')
	print('Player 1 :\n')
	print('	D : déplacement à droite\n')
	print('	Q : déplacement à gauche\n')
	print('	A : Saut vers la gauche\n')
	print('	E : Saut vers la droite\n')
	print('	Z : Attaquer\n')
	print('	S : Défense\n')
	print('\n')
	print('Player 2 :\n')
	print('	-> : déplacement à droite\n')
	print('	<- : déplacement à gauche\n')
	print('	L : Saut vers la gauche\n')
	print('	M : Saut vers la droite\n')
	print('	O : Attaquer\n')
	print('	P : Défense\n')

# affichage du menu pause durant une partie
def pause(save):
	option2()
	
	print(' 1 : Reprendre le jeu\n')
	if save == 0:
		print(colored(' 2 : Pas de partie sauvegardée\n', 'grey'))
	else:
		print(' 2 : Charger la dernière game\n')
	print(' 3 : Sauvegarder la partie\n')
	print(' 4 : Quittez le jeu\n')
	while True:
		option = input('entrez votre choix: ')
		option = ''
		option = input('Confirmez votre choix en entrant le numéro: ')
		#print(f'vous avez sélectionner \'{option}\'')
		if option == '1':
			return 1
		elif option == '2':
			return 2
		elif option == '3':
			return 3
		elif option == '4':
			return 4
		else:
			print('Veuillez entrer un choix existant dans le menu.\n')

# fonction qui démarre le jeu Fancy Fancer avec le menu	
def print_menu():
	os.system('clear')
	save = 0
	if os.path.getsize('./game.sav') != 0:
		save = 1
	menuP(save)
	p = True
	p1 = False
	
	pg.mixer.init()
	menu_song = pg.mixer.Sound('./song/menu_song.ogg')
	menu_song.set_volume(0.1)
	menu_song.play(loops=-1)
	
	while True:
		choix = input('Entrez votre choix: ')
		if choix == '1':
			p = False
			p1 = True
			option1()
		elif choix == '2':
			p = False
			option2()
			print('3 : Retour\n')
		elif choix == '0' and p:
			os.system('clear')
			print('Vous avez quittez le jeu. A bientôt !\n')
			break
		elif choix == '3':
			p = True
			p1 = False
			menuP(save)
		elif choix == 'B1' and p1:
			l = charge_background(1)
			p1 = 0
			p2 = 0
			x = []
			for i in range(len(l)):
				if l[i] == '1':
					p1 = (i+1)*100//len(l)
				if l[i] == '2':
					p2 = 100 - ((len(l)-i)*100//len(l))
				if l[i] == 'x':
					x.append((i+1)*100//len(l))	
			menu_song.stop()	
			run(p1,p2,x,1)
			break
		elif choix == 'B2' and p1:
			l = charge_background(0)
			p1 = 0
			p2 = 0
			x = []
			for i in range(len(l)):
				if l[i] == '1':
					p1 = (i+1)*100//len(l)
				if l[i] == '2':
					p2 = (i+1)*100//len(l)
				if l[i] == 'x':
					x.append((i+1)*100//len(l))	
			menu_song.stop()	
			run(p1,p2,x,0)
			break
		elif choix == 'delete' and p:
			conf = input('Confimez la suppression (apppuyer sur ENTRER) ?')
			if conf == "":
				open('./game.sav', 'w').close()	
			os.system('clear')
			save = 0
			menuP(save)
		else:
			print('Veuillez entrer un choix existant dans le menu.\n')
		
