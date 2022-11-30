# Classe player pour la version terminale
# 11-2022

import time

class player():
	
	def __init__(self,carte,x,y,np,width):
		self.width = width
		self.np = np
		self.carte = carte
		self.h_pos = x
		self.w_pos = y
		self.score = 0
		self.speed = 1
		self.blockR = False
		self.blockL = False
		self.JR = False
		self.JL = False
		self.colR = set()
		self.colL = set()
		self.colJR = set()
		self.colJL = set()
		self.mv_speed = 1/10
		self.is_atk = False
		self.is_def = False
		self.atk_speed = 0.5
		self.atk_range = 1
	
	# modifie la matrice pour l'affichage orienté droite du personnage
	def displayerR(self):
		for i in range(5):
			for j in range(4):
				if i == 0 and j == 0:
					self.carte[self.h_pos+i][self.w_pos+j] = "<"
				elif i == 0 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "o"
				elif i == 0 and j == 2:
					self.carte[self.h_pos+i][self.w_pos+j] = ">"
				elif i == 1 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 1 and j == 2: 
					self.carte[self.h_pos+i][self.w_pos+j] = "_"
				elif i == 1 and j == 3:
					self.carte[self.h_pos+i][self.w_pos+j] = "/"
				elif i == 2 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 3 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 4 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 4 and j == 0:
					self.carte[self.h_pos+i][self.w_pos+j] = "/"
	
	# modifie la matrice pour l'affichage orienté gauche du personnage
	def displayerL(self):
		for i in range(5):
			for j in range(4):
				if i == 0 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "<"
				elif i == 0 and j == 2:
					self.carte[self.h_pos+i][self.w_pos+j] = "o"
				elif i == 0 and j == 3:
					self.carte[self.h_pos+i][self.w_pos+j] = ">"
				elif i == 1 and j == 2:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 1 and j == 1:
					self.carte[self.h_pos+i][self.w_pos+j] = "_"
				elif i == 1 and j == 0:
					self.carte[self.h_pos+i][self.w_pos+j] = "\\"
				elif i == 2 and j == 2:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 3 and j == 2:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 4 and j == 2:
					self.carte[self.h_pos+i][self.w_pos+j] = "|"
				elif i == 4 and j == 3:
					self.carte[self.h_pos+i][self.w_pos+j] = "\\"
	# ajoute le score de chaque
	def print_score(self):
		m = self.width//2
		if self.np:
			self.carte[5][m-1] = self.score
		else:
			self.carte[5][m+1] = self.score
	
	# efface le joueur de la matrice		
	def remove(self):
		for i in range(5):
			for j in range(4):
				self.carte[self.h_pos+i][self.w_pos+j] = " "			
	
	# réinitialise à vide l'ensemble colR et colL
	def update(self):
		self.colR = set()
		self.colL = set()
	
	# ajoute dans colL et colR les élements derrière et devant des joueurs
	def collision(self):
			for i in range(5):
				self.colR.add(self.carte[self.h_pos+i][self.w_pos+4])
				self.colL.add(self.carte[self.h_pos+i][self.w_pos-1])	
			if len(self.colR) != 1 :
				self.blockR = True
			else:
				self.blockR = False
			
			if len(self.colL) != 1 :
				self.blockL = True
			else:
				self.blockL = False
	
	# regarde si la zone d'atterissage su saut est possible ou pas
	def collisionJump(self):
		for i in range(5):
			for j in range(5):
				if self.w_pos+6+3 <= self.width:
					self.colJR.add(self.carte[self.h_pos+1+i][self.w_pos+5+j])
				if self.w_pos-6-3 >= 0:
					self.colJL.add(self.carte[self.h_pos+1+i][self.w_pos-6+j])
		if len(self.colJR) != 1 :
			self.JR = True
		else:
			self.JR = False
			
		if len(self.colJL) != 1 :
			self.JL = True
		else:
			self.JL = False
	
	# déplacement à droite			
	def moveR(self):
		self.collision()
		if self.w_pos < self.width -5 and not(self.blockR):
			self.remove()
			self.w_pos += 1
			if self.np:
				self.displayerR()
			else:
				self.displayerL()
		self.update()
	
	# déplacement à gauche
	def moveL(self):
		self.collision
		if self.w_pos > 1 and not(self.blockL):
			self.remove()
			self.w_pos -= 1
			if self.np:
				self.displayerR()
			else:
				self.displayerL()
		self.update()
	
	# déplacement vers le haut d'une case	
	def moveUP(self):
		if self.h_pos > 0:
			time.sleep(self.mv_speed)
			self.remove()
			self.h_pos -= 1
			if self.np:
				self.displayerR()
			else:
				self.displayerL()
	
	# déplacement vers le bas d'une case
	def moveDOWN(self):
			time.sleep(self.mv_speed)
			self.remove()
			self.h_pos += 1
			if self.np:
				self.displayerR()
			else:
				self.displayerL()
	
	# saut à droite	
	def jumpR(self):
		self.collisionJump()
		if self.w_pos+6 < self.width -5 and not(self.JR):
			time.sleep(self.mv_speed)
			self.remove()
			self.w_pos += 6
			if self.np:
				self.displayerR()
			else:
				self.displayerL()
		self.colJR = set()
		self.colJL = set()
	
	# saut à gauche	
	def jumpL(self):
		self.collisionJump()
		if self.w_pos-6 > 1 and not(self.JL) :
			time.sleep(self.mv_speed)
			self.remove()
			self.w_pos -= 6
			if self.np:
				self.displayerR()
			else:
				self.displayerL()		
		self.colJR = set()
		self.colJL = set()
	
	# revient à l'état standard du personnage
	def release(self):
		if self.np:
			self.carte[self.h_pos+1][self.w_pos+3] = "/"		
		else:
			self.carte[self.h_pos+1][self.w_pos] = "\\"
	
	# mouvement attaquer			
	def attaque(self):
		if self.np:
			self.carte[self.h_pos+1][self.w_pos+3] = "_"
			if self.carte[self.h_pos+1][self.w_pos+3+self.atk_range] != " ":
				self.is_atk = True
		else:
			self.carte[self.h_pos+1][self.w_pos] = "_"
			if self.carte[self.h_pos+1][self.w_pos-self.atk_range] != " ":
				self.is_atk = True
				
	# mouvement défense	
	def defense(self):
		if self.np:
			self.carte[self.h_pos+1][self.w_pos+3] = "|"
			self.is_def = True
		else:
			self.carte[self.h_pos+1][self.w_pos] = "|"
			self.is_def = True
		
	
