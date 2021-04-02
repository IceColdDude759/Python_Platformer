import pygame
from spritesheetparser import Spritesheet

class ModifiedGroup(pygame.sprite.Group):
	def __init__(self, engine):
		pygame.sprite.Group.__init__(self)
		self.engine = engine
	def draw(self):
		sprites = self.sprites()
		for spr in sprites:
			self.engine.screen.blit(spr.image, (spr.rect.x - self.engine.camera.offset.x, spr.rect.y - self.engine.camera.offset.y))


class Player(pygame.sprite.Sprite):
	def __init__(self,engine):
		pygame.sprite.Sprite.__init__(self)
		self.engine = engine
		self.is_jumping, self.on_ground = True,True
		#False, False
		self.facing_right = True
		self.gravity, self.friction = .35, -.09
		self.load()
		self.rect = self.image.get_rect()
		self.rect.w, self.rect.h = 27, 55
		self.position = pygame.math.Vector2(self.engine.world.start_x, self.engine.world.start_y)
		self.velocity = pygame.math.Vector2(0,0)
		self.acceleration = pygame.math.Vector2(5,self.gravity)
		self.max_vel = 6
		self.index = 0
		self.tick = 0
		self.bump = False
		self.health = engine.health
		self.coin = engine.coin
		
		self.loop_delay = True


	def draw(self):
		self.animate()

		self.engine.screen.blit(self.image, (self.rect.x -12 - self.engine.camera.offset.x, self.rect.y -24 - self.engine.camera.offset.y))


	def update(self):
		#print(self.on_ground, self.velocity.y)
		#print(self.rect)
		#print(self.rect.w)
		self.vertical_movement(self.engine.dt)
		self.checkCollisionsy(self.engine.tiles)
		
		self.horizontal_movement(self.engine.dt)
		self.checkCollisionsx(self.engine.tiles)

		self.checkOtherCollision()
		self.health_check()


	def img_load(self, name):
	
		img = pygame.image.load(name+".png")
		img = pygame.transform.scale(img, (50, 80))
		return img


	def animate (self):
			

		if self.engine.game_state == -1:
			#death animeation
			death=self.position.y
			self.loop_delay = not(self.loop_delay)
			if self.rect.y > death-200 and self.loop_delay:
				self.image = self.dead_img
				self.rect.y -= 1
		else :
			#jump animeation
			if  self.is_jumping and self.velocity.y < 0 and not(self.on_ground):
				if self.facing_right:
					self.image = self.jump_img[0]
				else:
					self.image = self.jump_img[2]
				return
			if self.is_jumping and self.velocity.y > 0 and not(self.on_ground):
				if self.facing_right:
					self.image = self.jump_img[1]
				else:
					self.image = self.jump_img[3]
				return

			#walk animation
			self.tick += self.engine.tick
			if self.velocity.x != 0 and self.on_ground and self.tick > 80:
				self.tick = 0
				self.index +=1
				if self.index >= len(self.right_img):
					self.index = 0
				if self.velocity.x > 0 :
					self.image = self.right_img[self.index]
				elif self.velocity.x < 0 :
					self.image = self.left_img[self.index]
				return
			#idle animation
			if 	self.velocity.x == 0 and self.on_ground and self.tick > 150 :
				self.image = self.idle_img
				
			

	def load(self):
		self.char_name = "character/character_robot_"
		self.left_img = []
		self.right_img = []
		self.jump_img = []
		self.idle_img = self.img_load(self.char_name +"idle")
		self.dead_img = self.img_load('img/player/1g2')

		for i in range(0,8):
			self.right_img.append(self.img_load(self.char_name +f"walk{i}"))

		for i in range(0,8):
			self.left_img.append(pygame.transform.flip(self.right_img[i], True, False))

		for i in range(0,2):
			self.jump_img.append(self.img_load(self.char_name +f"jump{i}"))

		for i in range(0,2):
			self.jump_img.append(pygame.transform.flip(self.jump_img[i] ,True, False))

		self.coin_fx = pygame.mixer.Sound('img/coin.wav')
		self.coin_fx.set_volume(0.5)
		self.image = self.idle_img


	def horizontal_movement(self,dt):		
		self.acceleration.x = 0
		if self.engine.LEFT_KEY and not self.bump:
			self.acceleration.x -= .6
		elif self.engine.RIGHT_KEY and not self.bump:
			self.acceleration.x += .6
		self.acceleration.x += self.velocity.x * self.friction
		self.velocity.x += self.acceleration.x * dt
		self.limit_x_velocity(self.max_vel)
		self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
		self.rect.x = self.position.x
		

	def vertical_movement(self,dt):
		if self.on_ground:
			self.is_jumping = True
			self.on_ground = False
			if self.engine.SPACE_KEY :
				self.velocity.y -= 8
		   
		self.velocity.y += self.acceleration.y * dt
		self.limit_y_velocity(10)
		self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
		self.rect.bottom = self.position.y
		

	def limit_x_velocity(self, max_vel):
		self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
		if abs(self.velocity.x) < .31: self.velocity.x = 0


	def limit_y_velocity(self, max_vel):
		self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
		if abs(self.velocity.y) < .31: self.velocity.y = 0


	def get_hits(self, tiles):
		hits = []
		for tile in tiles:
			if self.rect.colliderect(tile):
				if tile.can_collide :
					hits.append(tile)
					#print(tile.rect)
		return hits


	def checkCollisionsx(self, tiles):
		collisions = self.get_hits(tiles)
		self.bump = False
		for tile in collisions:
			if self.velocity.x > 0:  # Hit tile moving right
				self.position.x = tile.rect.left - self.rect.w
				self.rect.x = self.position.x 
				self.velocity.x = 0
				self.bump = True
			elif self.velocity.x < 0:  # Hit tile moving left
				self.position.x = tile.rect.right
				self.rect.x = self.position.x 
				self.velocity.x = 0
				self.bump = True
		
			
	def checkCollisionsy(self, tiles):
		self.on_ground = False
		self.rect.bottom += 1
		collisions = self.get_hits(tiles)
		for tile in collisions:
			if self.velocity.y > 0:  # Hit tile from the top
				self.on_ground = True
				self.is_jumping = False
				self.velocity.y = 0
				self.position.y = tile.rect.top
				self.rect.bottom = self.position.y
			elif self.velocity.y < 0:  # Hit tile from the bottom
				self.velocity.y = 0
				self.position.y = tile.rect.bottom + self.rect.h
				self.rect.bottom = self.position.y


	def checkOtherCollision(self):
		#check for collision with enemies ,lava , exit, coin ,etc.
		if pygame.sprite.spritecollide(self, self.engine.enemy_group, True):
			#self.velocity.x -= 3
			self.health -= 1

		if pygame.sprite.spritecollide(self, self.engine.lava_group, False):
			self.engine.game_state = -1	
		
		if pygame.sprite.spritecollide(self, self.engine.exit_group, False):
			self.engine.game_state = 1	

		if pygame.sprite.spritecollide(self, self.engine.coin_group, True):
			self.coin += 1
			self.coin_fx.play()


	def health_check(self):
		if self.health <= 0 :
			self.engine.game_state = -1
		if self.velocity.x > 0 :
			self.facing_right = True
		if self.velocity.x < 0 :
			self.facing_right = False	
		
		if self.position.x > self.engine.right_border or self.position.y > self.engine.bottom_border :
			self.position = pygame.math.Vector2(self.engine.world.start_x, self.engine.world.start_y)