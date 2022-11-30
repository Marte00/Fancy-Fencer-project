# le code du listener vient du doc
#https://pynput.readthedocs.io/en/latest/keyboard.html
#
# ce fichier contient le code principale du jeu 
# 11-2022

import os
from player_t import player
import time
from pynput import keyboard
import menu
import pygame as pg


#------------------- function --------------------------#
# liste des touches appuyés
is_press = []

# gestion des touches
def on_press(key):
	global is_press
	if key not in is_press:
		if key == keyboard.KeyCode.from_char('d'):
			is_press.append('d')
			
		if key == keyboard.KeyCode.from_char('q'):
			is_press.append('q')
		
		if key == keyboard.KeyCode.from_char('e'):
			is_press.append('e')
		
		if key == keyboard.KeyCode.from_char('a'):
			is_press.append('a')
		
		if key == keyboard.KeyCode.from_char('l'):
			is_press.append('l')
		
		if key == keyboard.KeyCode.from_char('m'):
			is_press.append('m')
			
		if key == keyboard.Key.right:
			is_press.append('right')
			
		if key == keyboard.Key.left:
			is_press.append('left')
			
		if key == keyboard.KeyCode.from_char('z'):
			is_press.append('z')
			
		if key == keyboard.KeyCode.from_char('o'):
			is_press.append('o')
		
		if key == keyboard.KeyCode.from_char('s'):
			is_press.append('s')
		
		if key == keyboard.KeyCode.from_char('p'):
			is_press.append('p')
		
		if key == keyboard.KeyCode.from_char('n'):
			is_press.append('n')

# affiche matrice
def print_map(carte):
	for i in carte :
		for j in i:
			print(j,end='')
		print('')
		
#------------- main ----------------------#

def run(w_pos1,w_pos2,x,BG):	
	global is_press
	save = 0
	# taille de la map
	background = BG
	heigh = 25
	width = 100

	# initialise la map
	carte = [["#"]*width if i == heigh -1 else [" "]*width for i in range(heigh) ]
	for i in range(width):
		carte[0][i] = "-"
	for i in range(1,heigh-1):
		carte[i][0] = "|"
		carte[i][99] = "|"
	mid = width//2
	carte[5][mid-2] = "|"; carte[5][mid] = "|" ; carte[5][mid+2] = "|"
	for i in x:
		if 0 < i < w_pos1 or w_pos1+4 < i < w_pos2 or w_pos2 + 4 < i < width-1:
				carte[23][i] = "x"
		if w_pos1 < i < w_pos1+4 or w_pos2 < i < w_pos2+4: 
			if i + 4 < width-1:
				carte[23][i+4] = "x"
	# parametre
	h_pos = 19
	frame = 1/60
	P1 = 1
	P2 = 0
	activate = True
	
	# parametre player
	# player 1
	w_pos1 = w_pos1
			
	# player 2
	w_pos2 = w_pos2

	# init player
	p1 = player(carte,h_pos,w_pos1,1,width)
	p2 = player(carte,h_pos,w_pos2,0,width)
	p1.displayerR()
	p2.displayerL()
	p1.print_score()
	p2.print_score()
	
	# ...or, in a non-blocking fashion:
	listener = keyboard.Listener(
	    on_press=on_press)
	listener.start()

	# affichage de la matrice 
	os.system('clear')
	print_map(carte)
	
	# son
	pg.mixer.init()
	battle_song = pg.mixer.Sound('./song/battle.mp3')
	battle_song.set_volume(0.1)
	atk_sound = pg.mixer.Sound('./song/attaque_effect.wav')
	saut_sound = pg.mixer.Sound('./song/saut.wav')
	def_sound = pg.mixer.Sound('./song/defense.wav')
	move_sound = pg.mixer.Sound('./song/moveg.flac')
	atk_sound.set_volume(0.1)
	saut_sound.set_volume(0.1)
	def_sound.set_volume(0.1)
	move_sound.set_volume(0.05)
	while True:		
				# lance la music
				if activate:
					battle_song.play(loops=-1)
					activate = False
				# vérifie si le fichier de sauvegarde est vide ou pas	
				if os.path.getsize('./game.sav') != 0:
					save = 1
				
				# touche pause				
				if "n" in is_press:
					battle_song.stop()
					choix = menu.pause(save)
					
					# Quitte le jeu en terminant la boucle de jeu
					if choix == 4:
						os.system('clear')
						print('Vous avez quittez le jeu. A bientôt !\n')
						break
						
					# charge les données depuis le fichier de sauvegarde
					elif choix == 2:
						l = menu.charge_game()
						p1.remove(); p2.remove()
						background = l[0]
						p1.w_pos = l[1]; p2.w_pos = l[2]; p1.score = l[3]; p2.score = l[4]
						p1.displayerR(); p2.displayerL(); p1.print_score(); p2.print_score()
						for i in range(width-1):
							if carte[23][i] == "x":
								carte[23][i] = " "
						for i in menu.change_background(background):
							carte[23][i] = "x"
						os.system("clear")
						print_map(carte)
						is_press.remove('n')	
					
					# enregistre dans un fichier des données
					elif choix == 3:
						with open("./game.sav", "w") as f:
							f.write(f"{background}\n")
							f.write(f"{p1.w_pos}\n")
							f.write(f"{p2.w_pos}\n")
							f.write(f"{p1.score}\n")
							f.write(f"{p2.score}\n")
							
					# sinon continue la partie
					else:
						activate = True
						os.system("clear")
						print_map(carte)
						is_press.remove('n')	
					
				p1.collision()			
				p2.collision()
				
				# -------- p1 ---------#
					
				# deplacement à droite
				if 'd' in is_press and not(p1.blockR) :
					move_sound.play()
					p1.moveR()
					os.system("clear")
					print_map(carte)
					is_press.remove('d')
					
								
				# deplacement à gauche		
				if 'q' in is_press and not(p1.blockL):
					move_sound.play()
					p1.moveL()
					os.system("clear")
					print_map(carte)
					is_press.remove('q')
				
				# saut à droite
				if 'e' in is_press :
					saut_sound.play()
					p1.moveUP()
					os.system("clear")
					print_map(carte)
					p1.jumpR()
					os.system("clear")
					print_map(carte)
					p1.moveDOWN()
					os.system("clear")
					print_map(carte)
					is_press.remove('e')
				
				# saut à gauche
				if 'a' in is_press :
					saut_sound.play()
					p1.moveUP()
					os.system("clear")
					print_map(carte)
					p1.jumpL()
					os.system("clear")
					print_map(carte)
					p1.moveDOWN()
					os.system("clear")
					print_map(carte)
					is_press.remove('a')
				
				# attaque
				if 'z' in is_press:
					atk_sound.play()
					p1.attaque()
					os.system("clear")
					print_map(carte)
					timer = 0
					while timer < p1.atk_speed:
						if p2.is_def == True:
							p1.release()
							p1.is_atk = False
						if p2.is_atk == True:
							p1.w_pos = w_pos1; p2.w_pos = w_pos2
							p1.displayerR(); p2.displayerL()
						time.sleep(0.1)
						timer += 0.1
					p1.release()
					if p1.is_atk:
						p1.score += 1
						p1.print_score()
					p1.is_atk = False 
					os.system("clear")
					print_map(carte)	
					is_press.remove('z')
				
				# défense
				if 's' in is_press:
					def_sound.play()
					p1.defense()
					os.system("clear")
					print_map(carte)
					timer = 0
					while timer < p1.atk_speed:
						p1.is_def = True
						time.sleep(0.1)
						timer += 0.1
					p1.is_def = False
					p1.release()
					os.system("clear")
					print_map(carte)
					is_press.remove('s')
					
				#------------ player 2 ----------#
				
				# déplacement à droite
				if 'right' in is_press and not(p2.blockR) :
					move_sound.play()
					p2.moveR()
					os.system("clear")
					print_map(carte)
					is_press.remove('right')
				# deplacement à gauche		
				if 'left' in is_press and not(p2.blockL):
					move_sound.play()
					p2.moveL()
					os.system("clear")
					print_map(carte)
					is_press.remove('left')
				
				# saut à droite
				if 'm' in is_press:
					saut_sound.play()
					p2.moveUP()
					os.system("clear")
					print_map(carte)
					p2.jumpR()
					os.system("clear")
					print_map(carte)
					p2.moveDOWN()
					os.system("clear")
					print_map(carte)
					is_press.remove('m')
				
				# saut à gauche
				if 'l' in is_press :
					saut_sound.play()
					p2.moveUP()
					os.system("clear")
					print_map(carte)
					p2.jumpL()
					os.system("clear")
					print_map(carte)
					p2.moveDOWN()
					os.system("clear")
					print_map(carte)
					is_press.remove('l')
				# attaque
				if 'o'	in is_press:
					atk_sound.play()
					p2.attaque()
					os.system("clear")
					print_map(carte)
					timer = 0
					while timer < p2.atk_speed:
						if p1.is_def == True:
							p2.release()
							p2.is_atk = False
						if p1.is_atk == True:
							p1.w_pos = w_pos1; p2.w_pos = w_pos2
							p1.displayerR(); p2.displayerL()
						time.sleep(0.1)
						timer += 0.1
					p2.release()
					if p2.is_atk:
						p2.score += 1
						p2.print_score()
					p2.is_atk = False 
					os.system("clear")
					print_map(carte)
					is_press.remove('o')
				#défense
				if 'p' in is_press:
					def_sound.play()
					p2.defense()
					os.system("clear")
					print_map(carte)
					timer = 0
					while timer < p2.atk_speed:
						p2.is_def = True
						time.sleep(0.1)
						timer += 0.1
					p2.is_def = False
					p2.release()
					os.system("clear")
					print_map(carte)
					is_press.remove('p')
					
				# met à jour les collisions		
				p1.update()
				p2.update()
				time.sleep(frame)
			
