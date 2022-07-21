import pygame, csv, os


class Enemy1(pygame.sprite.Sprite):

	def __init__(self, x, y,q):
		pygame.sprite.Sprite.__init__(self)
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.size = (40, 40)
		for num in range(1, 6):
			img_left = pygame.image.load(f'img/blob/l{num}.png')
			img_right = pygame.image.load(f'img/blob/r{num}.png')
			img_right = pygame.transform.scale(img_right, self.size)
			img_left = pygame.transform.scale(img_left, self.size)
			self.images_left.append(img_left)
			self.images_right.append(img_right)
		for num in range(1, 6):
			img_left = pygame.image.load(f'img/blob/l{num}.png')
			img_right = pygame.image.load(f'img/blob/r{num}.png')
			img_right = pygame.transform.scale(img_right, self.size)
			img_left = pygame.transform.scale(img_left, self.size)
			img_left = pygame.transform.flip(img_right, True, False)
			img_right = pygame.transform.flip(img_left, True, False)
			self.images_left.append(img_left)
			self.images_right.append(img_right)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0
		self.x_correction=0
		self.direction=False
		self.tick = 0

	def update(self,tick):
		walk_cooldown = 15
		self.tick += tick

		#update movemnets
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 63:
			 
			self.direction = not(self.direction)
			self.move_direction *= -1
			self.move_counter *= -1
			#print(self.move_direction)

		#update animation
		if abs(self.move_counter) > walk_cooldown and self.tick > 32:
			self.tick=0
			self.counter = 0	
			self.index += 1
			if self.index >= len(self.images_right) or self.index >= len(self.images_left) :
				self.index = 0
			if  self.move_direction == 1:
				self.image = self.images_right[self.index]
			if  self.move_direction == -1:
				self.image = self.images_left[self.index]


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y,tile_size):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.tick = 0

	def update(self,tick):
		self.tick +=tick
		# To animate the lava //in ms 4fps
		if self.tick > 250 :
			self.tick = 0
			self.image = pygame.transform.flip(self.image, True, False)


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y,tile_size):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size//2, tile_size//2))
		self.rect = self.image.get_rect()
		self.rect.x = x + tile_size//4
		self.rect.y = y + tile_size//4
		self.tick = 0


class Enemy2(pygame.sprite.Sprite):
	def __init__(self, x, y,tile_size):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size//2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.tick = 0
	

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y,tile_size):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/Exit.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size * 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y - tile_size
		self.tick = 0


class Tile(pygame.sprite.Sprite):
	def __init__(self, image, x, y, spritesheet,can_collide):
		pygame.sprite.Sprite.__init__(self)
		self.image = spritesheet.get_sprite(image)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.can_collide = can_collide

	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
	def __init__(self, filename, spritesheet, engine):
		self.engine = engine
		self.tile_size = self.engine.tile_size
		self.start_x, self.start_y = 0, 0
		self.spritesheet = spritesheet
		self.tiles = self.load_tiles(filename)
		self.map_surface = pygame.Surface((self.map_w, self.map_h))
		self.map_surface.set_colorkey((0, 0, 0))
		self.load_map()

	def draw_world(self):
		self.engine.screen.blit(self.map_surface, (0 - self.engine.camera.offset.x, 0 - self.engine.camera.offset.y))

	def load_map(self):
		for tile in self.tiles:
			tile.draw(self.map_surface)

	def read_csv(self, filename):
		map = []
		with open(os.path.join(filename)) as data:
			data = csv.reader(data, delimiter=',')
			for row in data:
				map.append(list(row))
		return map

	def load_tiles(self, filename):
		tiles = []
		map = self.read_csv(filename)
		x, y = 0, 0
		for row in map:
			x = 0
			for tile in row:
				if tile == '0':
					self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
				elif tile == '1':
					tiles.append(Tile('dirt2.png', x * self.tile_size, y * self.tile_size, self.spritesheet, True))
				elif tile == '2':
					tiles.append(Tile('dirt3.png', x * self.tile_size, y * self.tile_size, self.spritesheet, True))
				elif tile == '3':
					self.engine.coin_group.add(Coin(x * self.tile_size, y * self.tile_size,self.tile_size))
				elif tile == '4':
					self.engine.exit_group.add(Exit(x * self.tile_size, y * self.tile_size,self.tile_size))
				elif tile == '6':
					self.engine.enemy_group.add(Enemy1(x * self.tile_size, y * self.tile_size,self.tile_size))
				elif tile == '7':
					self.engine.lava_group.add(Lava(x * self.tile_size, y * self.tile_size,self.tile_size))
					# Move to next tile in current row
				x += 1

			# Move to next row
			y += 1
			# Store the size of the tile map
		self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
		return tiles





