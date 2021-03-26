import pickle
import pygame
from pygame.locals import *
#from player import Player as p2

pygame.init()

clock = pygame.time.Clock()
FPS = 60
##############################################################################
####################### FILE/LEVEl TO EDIT HERE ##############################
level = 0
##############################################################################
##############################################################################

screen_width = 780
screen_height = 450
tile_size = 30
map_size = screen_width * 5

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('aNI ')

#define game variables
#tile_size = 25
no_of_tile=screen_width/tile_size
#layer=int(screen_height/tile_size)
no_of_tile=screen_width//tile_size
middle_tile = no_of_tile//2

#load images
#############################################################################
#############################################################################
################################## ADD TEXTURE HERE##########################
#############################################################################
img_array=[]
img_array.append(pygame.image.load('img/dirt3.png'))
img_array.append(pygame.image.load('img/dirt2.png'))
img_array.append(pygame.image.load('img/lava.png'))
img_array.append(pygame.image.load('img/coin.png'))
img_array.append(pygame.image.load('img/enemy1.png'))
img_array.append(pygame.image.load('img/Exit.png'))

#img_array.append(pygame.image.load('images.jpg').convert())


############################################################################
############################################################################
############################################################################
############################################################################
############################################################################
#sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/Backg.png')
bg_img = pygame.transform.scale(bg_img, (screen_width,screen_height))




def draw_grid():
	for line in range(0, 100):#game window /tile size
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player():
	def __init__(self,x,y): 
		self.image = pygame.image.load("img/player/guy_1.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (30, 60))
		self.surf = pygame.Surface((20, 20))
		self.rect = self.surf.get_rect(center = (160, 220))
		
		
	def move(self):
		pressed_keys = pygame.key.get_pressed()	 
		if self.rect.left > 0:
			  if pressed_keys[K_LEFT]:
				  self.rect.move_ip(-15, 0)
		if self.rect.right < map_size:		
			  if pressed_keys[K_RIGHT]:
				  self.rect.move_ip(15, 0)


class World():
	def __init__(self, data):
		self.all_tile_list = []
		self.current_tile_list=[]

		strip_count = 0
		for strip in data:
			block_count = 0
			temp_strip=[]
			for tile in strip:
				"""if tile == 0:
					img = pygame.transform.scale(dirt_img, (10,10))
					img_rect = img.get_rect()
					img_rect.x = block_count * 10
					img_rect.y = 0
					tile = (img, img_rect)
					temp_strip.append(tile)"""
				if tile == 1:
					img = pygame.transform.scale(img_array[0], (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = strip_count * tile_size
					img_rect.y = block_count * tile_size
					tile = (img, img_rect)
					temp_strip.append(tile)
				elif tile == 2:
					img = pygame.transform.scale(img_array[1], (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = strip_count * tile_size
					img_rect.y = block_count * tile_size
					tile = (img, img_rect)
					temp_strip.append(tile)
				elif tile == 3:
					img = pygame.transform.scale(img_array[2], (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = strip_count * tile_size
					img_rect.y = block_count * tile_size
					tile = (img, img_rect)
					temp_strip.append(tile)
				elif tile == 4:
					img = pygame.transform.scale(img_array[3], (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = strip_count * tile_size
					img_rect.y = block_count * tile_size
					tile = (img, img_rect)
					temp_strip.append(tile)
				elif tile == 5:
					img = pygame.transform.scale(img_array[4], (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = strip_count * tile_size
					img_rect.y = block_count * tile_size
					tile = (img, img_rect)
					temp_strip.append(tile)
				elif tile == 6:
					img = pygame.transform.scale(img_array[5], (tile_size, tile_size*2))
					img_rect = img.get_rect()
					img_rect.x = strip_count * tile_size
					img_rect.y = block_count * tile_size
					tile = (img, img_rect)
					temp_strip.append(tile)
				block_count += 1
			self.all_tile_list.append(temp_strip)
			strip_count += 1
		#print(self.all_tile_list)

	def draw(self):
		player_block=player.rect[0]//tile_size
		no_of_tile=screen_width//tile_size
		middle = no_of_tile//2
		start=player_block-middle
		if start<0:
			start=0
		self.current_tile_list=self.all_tile_list[start:(start+no_of_tile)]
		#print(current_tile_list)

		for strip in self.current_tile_list:
			for tile in strip:
				#print(tile[1])
				tile[1][0]=tile[1][0]-(start*tile_size)
				screen.blit(tile[0], tile[1])	

def change_world_data(img_array_num,coordinates):
	#print("change world called")
	#print(coordinates[1])
	#print(coordinates[0])
	try:
		world_data[coordinates[1]][coordinates[0]]=img_array_num
	except IndexError:
		print ("OUT OF ARRAY data")
	#print(world_data)

def delete_world_data(coordinates):
	#print("change world called")
	world_data[coordinates[1]][coordinates[0]]=0
	#print(world_data)

#top to bottom  strip update

with open(f"data{level}.ani","rb") as f:
	world_data=pickle.load(f)

#f.close()


player = Player(500, 400)

#world = World(world_data)


counter_for_selected_img=1

run = True
while run:

	clock.tick(FPS)

	screen.blit(bg_img, (0, 0))
	#screen.blit(sun_img, (100, 100))
	world = World(world_data)
	world.draw()
	


	player_block = player.rect[0] // tile_size
	start = player_block - middle_tile
	if start < 0:
		start = 0

	pos = pygame.mouse.get_pos()#(y,x)
	mouse=pygame.mouse.get_pressed()
	x=pos[0]
	y=pos[1]
	keys = pygame.key.get_pressed()
	increment=0

	if player.rect[0]>screen_width:
		increment=int((player.rect[0]-(screen_width-100))/tile_size)+10
	
	

	if mouse[0]:
		#print(pos)
		for column in range(0,screen_height+tile_size,tile_size):
			if y<column:
				for row in range(0,screen_width+tile_size,tile_size):
					if x<row:
						coordinate=[(int((column-tile_size)/tile_size)),(int((row-tile_size)/tile_size+increment))]
						change_world_data(counter_for_selected_img,coordinate)
						break
				break

	if mouse[2]:
		#print(pos)
		for column in range(0,screen_height+tile_size,tile_size):
			if y<column:
				for row in range(0,screen_width+tile_size,tile_size):
					if x<row:
						coordinate=[(int((column-tile_size)/tile_size)),(int((row-tile_size)/tile_size)+increment)]
						delete_world_data(coordinate)
						break
				break
	
	
	player.move()
	screen.blit(player.image, player.rect)
	draw_grid()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			with open(f"data{level}.ani","wb") as f:
				pickle.dump(world_data,f)


			#print(world_data)
			run = False
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_UP:
				if counter_for_selected_img>=len(img_array):
					counter_for_selected_img=1
				else :
					counter_for_selected_img+=1
			print(counter_for_selected_img)
		cursor = pygame.transform.scale(img_array[counter_for_selected_img-1], (tile_size, tile_size))
		#pygame.mouse.set_visible(False)  # hide the cursor
		screen.blit(cursor, pos)
	pygame.display.update()

pygame.quit()