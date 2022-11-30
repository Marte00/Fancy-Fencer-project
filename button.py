#https://www.youtube.com/watch?v=2iyx8_elcYg
# ce code a été pris sur la vidéo youtube ci-dessus
# elle a été modifier pour être adapté pour mon code
# l'effet sonore des touches a été ajouté

import pygame as pg

class Button():
	
	def __init__(self,x,y,image,scale):
		self.image = pg.transform.scale(image, (int(image.get_width()*scale),int(image.get_height()*scale) ))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.clicked = False
		
	def draw(self,screen):
		action = False
		
		# position du souris
		pos = pg.mouse.get_pos()
		
		# si la souris passe sur la zone de l'image
		if self.rect.collidepoint(pos):
			# si on clique 1 fois
			if pg.mouse.get_pressed()[0] and not(self.clicked):
				pg.mixer.init()
				button_song = pg.mixer.Sound('./song/button.mp3')
				button_song.set_volume(0.5)
				button_song.play()
				self.clicked = True
				action = True
		# si press 1 fois on ne represse plus
		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False
		# affichage du boutton
		screen.blit(self.image,(self.rect.x,self.rect.y))
		
		# renvoie vrai si cliquer dessus
		return action
