import pygame
from pygame.locals import Rect

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self,screen):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action



class Player():
	def __init__(self, x, y,tile_size,screen_width,screen_height,middle_tile):
		self.images_right = []
		self.images_left = []
		self.index = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/player/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (30, 60))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/player/1g2.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (50, 80))
		self.tile_size = tile_size
		self.screen_height = screen_height
		self.screen_width = screen_width
		self.middle_tile = middle_tile
		self.reset(x,y)
	def update(self,game_over,x_modifier,current_tile_list,screen,group):
		dx = 0
		dy = 0
		walk_cooldown = 5

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				#speed change here
				dx -= 7
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				#speed change here
				dx += 7
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y


			#check for collision
			self.in_air = False
			
			for strip in current_tile_list:
				for tile in strip:
					temp_rect=Rect(tile[1])
					temp_rect.x=temp_rect.x-(x_modifier*self.tile_size)
	
					#check for collision in x direction
					if temp_rect.colliderect(self.draw_rect.x + dx, self.draw_rect.y, self.width, self.height):
						dx = 0
						
					#check for collision in y direction
					#"""
					if temp_rect.colliderect(self.draw_rect.x, self.draw_rect.y + dy, self.width, self.height):
						#check if below the ground i.e. jumping
						if self.vel_y < 0:
							dy = temp_rect.bottom - self.draw_rect.top
							self.vel_y = 0
						#check if above the ground i.e. falling
						if self.vel_y >= 0:
							dy = temp_rect.y - self.draw_rect.bottom
							self.vel_y = 0
							self.in_air = False
					#"""
			

			#check for collision with enemies
			if pygame.sprite.spritecollide(self, group[0], True):
				self.health -= 1
			#check for collision with lava
			if pygame.sprite.spritecollide(self, group[1], False):
				game_over = -1	

			#to check for collision with exit
			if pygame.sprite.spritecollide(self, group[3], False):
				game_over = 1	

			
			#check player health
			if self.health < 1:
				game_over = -1

			#print(self.health)
			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


			#checks to prevent shit from happening
			
			self.draw_rect.x = self.middle_tile * self.tile_size
			
			if self.rect.bottom > self.screen_height:
				self.rect.bottom = self.screen_height
				dy = 0
			elif self.rect.top < 0:
				self.rect.top=0
			self.draw_rect.y = self.rect.y
			

		elif game_over == -1:
			self.image = self.dead_image
			if self.draw_rect.y > 50:
				self.draw_rect.y -= 8



		#draw player onto screen
		screen.blit(self.image, self.draw_rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
		pygame.draw.rect(screen, (255, 255, 255), self.draw_rect, 2)


		return game_over

	def reset(self,x,y):
		#if restart level then to reset the player to spawn
		self.index = 0
		self.counter = 0
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.draw_rect=self.image.get_rect()
		self.draw_rect.x = x
		self.draw_rect.y = y
		self.in_air = True
		self.health = 3

	
	
class ModifiedGroup(pygame.sprite.Group):
	def __init__(self,tile_size):
		pygame.sprite.Group.__init__(self)
		self.tile_size=tile_size

	def draw(self, surface,x_modifier):
		sprites = self.sprites()
		surface_blit = surface.blit
		for spr in sprites:
			correct_x=spr.rect.x-(x_modifier*self.tile_size)
			self.spritedict[spr] = surface_blit(spr.image, (correct_x,spr.rect.y))

