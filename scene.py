# class scene qui gere le déroulement de la partie combat


import pygame as pg
from player import Player
from button import Button
import menu
import os
class Scene:
	
	# init qui va créer une instance de la classe scene
	# création de l'écran de jeu
	def __init__ (self, screen):
		self.menuP = True
		self.pause = False
		self.screen = screen
		self.running = True
		self.option1 = False
		self.option2 = False
		self.bg = 1
		self.clock = pg.time.Clock()
		self.activate = True
		
		# création des joueurs
		self.y_p = 560
		self.x_p1 = 200
		self.x_p2 = 1000
		self.player1 = Player(self.x_p1,self.y_p,1)
		self.player2 = Player(self.x_p2,self.y_p,0)
		
		self.moving_sprite = pg.sprite.Group()
		self.moving_sprite.add(self.player1)
		self.moving_sprite.add(self.player2)
		self.collide_p = False
		
		# affichage du score
		self.font = pg.font.SysFont('monospace',25)
		
		self.score_png = pg.image.load('./image/score.png')
		self.img_score = pg.transform.scale(self.score_png,(200,100)) 
		
	
	
	# return Vrai si sprite1 et sprite2 sont en collisions sinon
	def collide(self,sprite1,sprite2):
		collide = pg.sprite.collide_rect(sprite1,sprite2)
		return collide
		
	# charge l'image de fond
	def background(self,img):
		background = pg.image.load(img)
		if self.bg == 2:
			self.screen.blit(background,(0,0))
		else:
			self.screen.blit(background,(0,0))
	# boucle de jeu
	def run(self):
		buttons = {
			'start' : pg.image.load('./image/start.png').convert_alpha(),
			'quit' : pg.image.load('./image/quit.png').convert_alpha(),
			'control' : pg.image.load('./image/control.png').convert_alpha(),
			'load' : pg.image.load('./image/load.png').convert_alpha(),
			'save' : pg.image.load('./image/save.png').convert_alpha(),
			'resume' : pg.image.load('./image/resume.png').convert_alpha(),
			'back' : pg.image.load('./image/back.png').convert_alpha(),
			'background1': pg.image.load('./image/default.jpg').convert_alpha(),
			'background2': pg.image.load('./image/aprem.jpg').convert_alpha()
		}
		
		startB = Button(430, 150, buttons['start'], 1)
		quitB = Button(432, 500, buttons['quit'], 1)
		quitB2 = Button(629, 550, buttons['quit'], 0.9)
		controlB = Button(435, 320, buttons['control'], 1.05)
		loadB = Button(630, 250, buttons['load'], 1)
		saveB = Button(637, 400, buttons['save'], 1)
		resumeB = Button(633, 90, buttons['resume'], 1)
		backB1 = Button(750, 200, buttons['back'], 1)
		backB2 = Button(430, 600, buttons['back'], 1)
		backg1B = Button(700, 350, buttons['background1'], 0.1)
		backg2B = Button(380, 350, buttons['background2'], 0.1)
		
		pg.mixer.init()
		menu_song = pg.mixer.Sound('./song/menu_song.ogg')
		menu_song.set_volume(0.1)
		menu_song.play(loops=-1)
		battle_song = pg.mixer.Sound('./song/battle.mp3')
		battle_song.set_volume(0.1)
		
		# si running est vrai on boucle
		while self.running:
			
			# si on n'est pas dans le menu principale
			if not(self.menuP):
				# si pas dans le menu pause
				if not(self.pause): 
					# active le son 1 fois
					if self.activate:	
						battle_song.play(loops=-1)
						self.activate = False
					# fond d'écran 
					if self.bg == 1:
						self.background('./image/default.jpg')
					if self.bg == 2:
						self.background('./image/aprem.jpg')
					# players
					self.screen.blit(self.player1.player_spriteSheet,self.player1.rect)
					self.screen.blit(self.player2.player_spriteSheet,self.player2.rect)
					
					# score
					self.print_score(self.player1.score, self.player2.score)
					self.screen.blit(self.img_score,(520,-20))
				else:
					# si dans le menu pause
					# song
					battle_song.stop()
					
					# affichage des controles des joueurs
					self.screen.fill((244,254,254))
					commande = pg.image.load('./image/controlp.png').convert_alpha()
					self.screen.fill((244,254,254))
					self.screen.blit(commande,(200,50))
					
					# continue la partie
					if resumeB.draw(self.screen):
						self.pause = False
					# quitter le jeu
					if quitB2.draw(self.screen):
						self.running = False
					# charge le fichier de sauvegarde et met à jour les données
					if loadB.draw(self.screen):
						# si fichier de sauvegarde non vide
						if os.path.getsize('./gamegraphique.sav') != 0:
							l = menu.charge_game2()
							self.bg = l[0]
							self.player1.rect.x = l[1]; self.player2.rect.x = l[2]; self.player1.score = l[3]; self.player2.score = l[4]
							self.player1.rect.y = l[5]; self.player2.rect.y = l[5]
							self.pause = False
							print('vous avez chargé une partie')
						else:
							print('Attention ! vous n\'avez pas de partie sauvegardé')
					# sauvegarde les données dans un fichier
					if saveB.draw(self.screen):
						with open("./gamegraphique.sav", "w") as f:
							f.write(f"{self.bg}\n")
							f.write(f"{self.player1.rect.x}\n")
							f.write(f"{self.player2.rect.x}\n")
							f.write(f"{self.player1.score}\n")
							f.write(f"{self.player2.score}\n")
							f.write(f"{self.player1.rect.y}\n")
						print('vous avez sauvegarder la partie')
			
			# si dans le menu principale			
			else:
				self.background('./image/foret.jpg')	
				# jouer
				if startB.draw(self.screen):
					self.option2 = True
				# quitter le jeu
				if quitB.draw(self.screen):
					self.running = False
					
				# affiche les controles des joueurs
				if controlB.draw(self.screen):
					self.option1 = True
				
				# si on choisi de voir les commandes des joueurs
				if self.option1:
					commande = pg.image.load('./image/controlp.png').convert_alpha()
					self.screen.fill((244,254,254))
					self.screen.blit(commande,(200,50))
					
					# retour menu principale
					if backB1.draw(self.screen):
						self.option1 = False
				# si on choisi l'option commencer
				if self.option2:
					self.background('./image/foret.jpg')
					# choix du background 1
					if backg1B.draw(self.screen):
						self.menuP = False
						menu_song.stop()
					# choix du background 2
					if backg2B.draw(self.screen):
						self.bg = 2
						self.player1.rect.y = 600
						self.player2.rect.y = 600
						self.menuP = False
						menu_song.stop()
					# retour au menu principale
					if backB2.draw(self.screen):
						self.option2 = False
			# event
			self.handling_events()
			self.moving_sprite.update()
			self.collide_p = self.collide(self.player1, self.player2)
			
			# on limite la vitesse de rafraichissement de l'écran à 60 fps
			self.clock.tick(60)
			pg.display.flip()
	
	# affiche le score	
	def print_score(self,a,b):
		self.score = self.font.render(f"{a} - {b}",1,(0,0,0))
		self.screen.blit(self.score,(580,60))
	
	# gestion des évenements 
	def handling_events(self):
		
		# son
		atk_sound = pg.mixer.Sound('./song/attaque_effect.wav')
		saut_sound = pg.mixer.Sound('./song/saut.wav')
		def_sound = pg.mixer.Sound('./song/defense.wav')
		move_sound = pg.mixer.Sound('./song/moveg.flac')
		atk_sound.set_volume(0.1)
		saut_sound.set_volume(0.1)
		def_sound.set_volume(0.1)
		move_sound.set_volume(0.05)
		
		# parcours les evenements dans la liste des evenement par la méthode get()
		for event in pg.event.get():
			if event.type ==  pg.QUIT: 
				self.running = False
			
			# si certaines touches sont appuyés
			if event.type == pg.KEYDOWN:
			
				if event.key == pg.K_z:
					atk_sound.play()
					if self.collide_p and self.player2.is_defending == False:
						self.player1.addScore()
				if event.key == pg.K_o:
					atk_sound.play()
					if self.collide_p and self.player1.is_defending == False:
						self.player2.addScore()
			
				if event.key == pg.K_n:
					self.pause = True
					self.activate = True
				
				if event.key == pg.K_a or event.key == pg.K_e or event.key == pg.K_l or event.key == pg.K_m:
					saut_sound.play()
					
				if event.key == pg.K_p or event.key == pg.K_s:	
					def_sound.play()
				
				if event.key == pg.K_q or event.key == pg.K_d or event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
					move_sound.play()
					
		# dictionnaire contenant les évenements des touches de clavier
		keys = pg.key.get_pressed()
		
		#-------------------- Joueur 1 ---------------------#
		
		# déplacement à droite
		if keys[pg.K_d] and not(keys[pg.K_z]):
			self.player1.move_right()
			
		# déplacement à gauche
		if keys[pg.K_q] and not(keys[pg.K_z]):
			self.player1.move_left()
			
		# saut à droite
		if keys[pg.K_e] and self.player1.jumpEnd:
			self.player1.isjumpR = True	
		if self.player1.isjumpR and not(self.player1.isjumpL) :
			self.player1.standby = False
			self.player1.jumpEnd = False
			self.player1.animate = True
			self.player1.jump(True)
			self.player1.move_right()	
		else:
			if self.player1.fin_a :
				self.player1.standby = True
				if self.player1.east:
					self.player1.load_animation('standbyR')
				if self.player1.west:
		    			self.player1.load_animation('standbyL')
		    				
		
		# saut à gauche
		if keys[pg.K_a] and self.player1.jumpEnd:
			self.player1.isjumpL = True		
		if self.player1.isjumpL and not(self.player1.isjumpR) :
			self.player1.standby = False
			self.player1.jumpEnd = False
			self.player1.animate = True
			self.player1.right = False
			self.player1.jump(False)
			self.player1.move_left()
		else:
			if self.player1.fin_a :
				self.player1.standby = True
				if self.player1.east:
					self.player1.load_animation('standbyR')
				if self.player1.west:
		    			self.player1.load_animation('standbyL')
			
		
		# attaquer
		if keys[pg.K_z] and not(keys[pg.K_q]) and not(keys[pg.K_d]):
			self.player1.standby = False
			if self.player1.east:
				self.player1.attaqueR()
			if self.player1.west:
	    			self.player1.attaqueL()
		else:
			if self.player1.fin_a :
				self.player1.standby = True
				self.player1.is_attacking = False;
				if self.player1.east:
					self.player1.rect.x
					self.player1.load_animation('standbyR')
				if self.player1.west:
		    			self.player1.load_animation('standbyL')
		    					

		# défendre
		if keys[pg.K_s] and not(keys[pg.K_q]) and not(keys[pg.K_d]) and not(keys[pg.K_z]):		    		
	    		self.player1.standby = False
	    		if self.player1.east:
	    			self.player1.defenseR()
	    		if self.player1.west:
	    			self.player1.defenseL()
		else:
	    		if self.player1.fin_a:
	    			self.player1.standby = True
	    			self.player1.is_defending = False;
	    			if self.player1.east:
	    				self.player1.load_animation('standbyR')
	    			if self.player1.west:
	    				self.player1.load_animation('standbyL')
	    		
	    		 	
	    			
		#-------------------- Joueur 2 ---------------------#
		
		
		# déplacement à droite
		if keys[pg.K_RIGHT] and not(keys[pg.K_o]):
			self.player2.move_right()
			
		
		# déplacement à gauche	
		if keys[pg.K_LEFT] and not(keys[pg.K_o]):
			self.player2.move_left()
		
		
		# saut à droite	
		if keys[pg.K_m] and self.player2.jumpEnd:
			self.player2.isjumpR = True		
		if self.player2.isjumpR and not(self.player2.isjumpL):
			self.player2.standby = False
			self.player2.jumpEnd = False
			self.player2.animate = True
			self.player2.jump(True)
			self.player2.move_right()
		else:
			
			if self.player2.fin_a:
				self.player2.standby = True
				if self.player2.east:
					self.player2.load_animation('standbyR')
				if self.player2.west:
		    			self.player2.load_animation('standbyL')	
		
		# saut à gauche	
		if keys[pg.K_l] and self.player2.jumpEnd:		
			self.player2.isjumpL = True		
		if self.player2.isjumpL and not(self.player2.isjumpR):
			
			self.player2.standby = False
			self.player2.jumpEnd = False
			self.player2.animate = True
			self.player2.right = False
			self.player2.jump(False)
			self.player2.move_left()
		else:
			if self.player2.fin_a:
				self.player2.standby = True
				if self.player2.east:
					self.player2.load_animation('standbyR')
				if self.player2.west:
		    			self.player2.load_animation('standbyL')
		
		
		# attaquer
		if keys[pg.K_o] and not(keys[pg.K_RIGHT]) and not(keys[pg.K_LEFT]):
			
			self.player2.standby = False
			if self.player2.east:
				self.player2.attaqueR()
			if self.player2.west:
	    			self.player2.attaqueL()
		else:
			if self.player2.fin_a:
				self.player2.standby = True
				self.player2.is_attacking = False;
				if self.player2.east:
					self.player2.load_animation('standbyR')
				if self.player2.west:
		    			self.player2.load_animation('standbyL')
		    			
		
		# défendre		
		if keys[pg.K_p] and not(keys[pg.K_RIGHT]) and not(keys[pg.K_LEFT]) and not(keys[pg.K_o]):		    		
	    		self.player2.standby = False
	    		if self.player2.east:
	    			self.player2.defenseR()
	    		if self.player2.west:
	    			self.player2.defenseL()
		else:
	    		if self.player2.fin_a:
	    			self.player2.standby = True
	    			self.player2.is_defending = False;
	    			if self.player2.east:
	    				self.player2.load_animation('standbyR')
	    			if self.player2.west:
	    				self.player2.load_animation('standbyL')
	
		if self.player1.is_attacking and self.player2.is_attacking:
			if self.collide_p:
				self.player1.rect.x = self.x_p1
				self.player2.rect.x = self.x_p2
				self.player1.score -= 1
				self.player2.score -= 1
		
			
			
