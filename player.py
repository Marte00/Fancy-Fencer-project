# class player pour la version graphique du jeu
import pygame as pg



# renvoie la liste de nos images 
def charge_animation(sprite_name,n,m):
	images = []
	path = f'player/{sprite_name}-'
	
	for i in range(n,m):
		image_path = path + str(i) + '.png'
		images.append(pg.image.load(image_path))
	
	return images
	

	
# dictionnaire des animations du joueur	
animations = {
	'standbyR' : charge_animation('player',24,32),
	'standbyL' : charge_animation('player',88,96), 
	'attaqueR' : charge_animation('player',32,40),
	'attaqueL' : charge_animation('player',96,104),
	'jumpR'    : charge_animation('player',19,23),
	'jumpL'    : charge_animation('player',83,87),
	'defenseR' : charge_animation('player',10,16),
	'defenseL' : charge_animation('player',74,80)
}


class Player(pg.sprite.Sprite):
	
	

	# init de notre instance player
	def __init__ (self, pos_x, pos_y, n_player):
		
		# appel au super class sprite qui instancie sprite
		super().__init__()

		
		# charge les images du player
		self.current_sprite = 0
		if n_player:
			self.sprite = animations.get('standbyR')
			self.east = True
			self.west = False
		else:
			self.sprite = animations.get('standbyL')
			self.east = False
			self.west = True
		self.player_spriteSheet = self.sprite[self.current_sprite]
		self.rect = self.player_spriteSheet.get_rect()
		
		# position de notre joueur sur la scene de jeus
		self.rect.x = pos_x
		self.rect.y = pos_y
		
		# gestion des animations 
		self.fin_a = False
		self.standby = True
		self.animate = False
		
		# vitesse de déplacement
		self.speed = 5
		
		# propriétés pour le saut & gestion de l'animation de saut
		self.gravity = 1 
		self.jumpcount = 10
		self.y_speed = self.jumpcount
		self.isjumpR = False
		self.isjumpL = False
		self.jumpEnd = True
		self.right = True
		
		# état attaque et défense
		self.is_attacking = False
		self.is_defending = False
		self.attaque_dist = 1
		
		# score du joueur
		self. score = 0
	
	# actualise en fonction du boucle de jeu les images
	def update(self):
		
		if not(self.animate):
			self.current_sprite += 0.15
			if self.current_sprite >= len(self.sprite) :
				self.current_sprite = 0
				if self.standby:
					self.fin_a = False		
				else:
					self.fin_a = True			
			self.player_spriteSheet = self.sprite[int(self.current_sprite)]
		else:
			if self.right:
				self.player_spriteSheet = pg.image.load('player/jumpR.png')
				self.animate = False
			else:
				self.player_spriteSheet = pg.image.load('player/jumpL.png')
				self.animate = False
				self.right = True
			
	
	# charge l'animation souhaiter	
	def load_animation(self,action):
		self.sprite = animations.get(action)	
	
	
	# se déplacer à droite
	def move_right(self):
		if self.rect.x < 1200:
			self.rect.x += self.speed	
		self.sprite = animations.get('standbyR')	
		self.east = True
		self.west = False
			
	
	# se déplacer à gauche
	def move_left(self):
		if self.rect.x >= -5:
			self.rect.x -= self.speed
		self.sprite = animations.get('standbyL')
		self.east = False
		self.west = True
	
	# saut vertical
	def jump(self,jump):
		self.rect.y -= self.y_speed
		self.y_speed -= self.gravity
		if  self.y_speed < -self.jumpcount:
			if jump:
				self.isjumpR = False
				self.jumpEnd = True	
			else:
				self.isjumpL = False
				self.jumpEnd = True
				
			self.y_speed = self.jumpcount
		
	
	# attaquer gauche
	def attaqueL(self):
		self.load_animation('attaqueL')
		self.is_attacking = True;
		
	
	#attaquer droite
	def attaqueR(self):
		self.load_animation('attaqueR')
		self.is_attacking = True;
		
	
	# defense gauche
	def defenseL(self):
		self.load_animation('defenseL')
		self.is_defending = True
	
	# défense droite
	def defenseR(self):
		self.load_animation('defenseR')
		self.is_defending = True
	
	# incrémente le score
	def addScore(self):
		self.score += 1
		
	
		
