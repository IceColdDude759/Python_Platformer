import pickle
import pygame
#from pygame.locals import *
from pygame import mixer
from model import *
from engine import World ,Coin


#pygame.mixer.pre_init(44100, -16, 2, 512)
#mixer.init()
pygame.init()

clock = pygame.time.Clock()
FPS = 60

#some game constant
screen_width = 800
screen_height = 450
tile_size = 25
level = 0
total_levels = 2


flags = pygame.RESIZABLE | pygame.SCALED
screen = pygame.display.set_mode((screen_width, screen_height), flags)
pygame.display.set_caption('BUG')


#font
font_1 = pygame.font.SysFont("Verdana", 100, True, True)
font = pygame.font.SysFont("Verdana", 70, True, True)
font_coin = pygame.font.SysFont("Verdana", 30)

#define game variables
player_spawn = (700,200)
game_over = 0
no_of_tile=screen_width//tile_size
middle_tile = no_of_tile//2
main_menu = False
coin = 0


#define colours
white = (255, 255, 255)
blue = (0, 0, 255)
red  = (20, 230, 255)


#load images
health_img = pygame.image.load('img/heart.png')
health_img = pygame.transform.scale(health_img,(30,30))
coin_img = pygame.image.load('img/coin.png')
coin_img = pygame.transform.scale(coin_img,(20,20))
bg_img = pygame.image.load('img/backg.png')
bg_img = pygame.transform.scale(bg_img, (screen_width,screen_height-tile_size*0))
restart_img = pygame.image.load('img/button/Restart.png')
restart_img = pygame.transform.scale(restart_img,(80,80))
start_img = pygame.image.load('img/button/Start.png')
start_img = pygame.transform.scale(start_img,(200,100))
exit_img = pygame.image.load('img/button/Exit.png')
exit_img = pygame.transform.scale(exit_img,(200,100))

#load Sound
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
#jump_fx = pygame.mixer.Sound('img/jump.wav')
#jump_fx.set_volume(0.5)
#game_over_fx = pygame.mixer.Sound('img/a.mp3')
#game_over_fx.set_volume(0.4)
#game_over_fx.play()
#



def draw_text(text, font, colour, x, y):
	img = font.render(text, True, colour)
	screen.blit(img, (x, y))

def reset_level (level):
	player.reset(player_spawn[0], player_spawn[1])
	enemy1_group.empty()
	lava_group.empty()
	exit_group.empty()
	coin_group.empty()

	#load in level data and create world
	file=open(f"data{level}.ani","rb")
	world_data = pickle.load(file)
	
	return world_data


#for loading levels 
file=open(f"data{level}.ani","rb")
world_data = pickle.load(file)

#f.close()


player = Player(player_spawn[0], player_spawn[1], tile_size, screen_width, screen_height, middle_tile)


enemy1_group = ModifiedGroup(tile_size)
lava_group = ModifiedGroup(tile_size)
coin_group = ModifiedGroup(tile_size)
enemy2_group = ModifiedGroup(tile_size)
exit_group = ModifiedGroup(tile_size)



group = [enemy1_group, lava_group, coin_group, exit_group, enemy2_group]

world = World(world_data, no_of_tile, tile_size, group)

restart_button = Button(screen_width // 2 -200, screen_height // 2 , restart_img)
start_button = Button(screen_width // 2 - 200, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 30, screen_height // 2, exit_img)
#print(world_data)




run = True
while run:
	current_tile_list=world.current_tile_list
	player_block = player.rect[0] // tile_size
	x_modifier = player_block - middle_tile
	if x_modifier < 0:
		x_modifier = 0
	

	screen.blit(bg_img, (0, 0))
	
	
	if main_menu :
		draw_text(' Ani GAME ', font_1, red, 100, 50)
		if exit_button.draw(screen):
			run = False
		if start_button.draw(screen):
			main_menu = False
	
	else :
		
		world.draw(screen,x_modifier)
		

		if game_over == 0:
			enemy1_group.update(x_modifier, clock.get_time())
			lava_group.update(clock.get_time())


			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				coin += 1
				coin_fx.play()
			screen.blit(coin_img, (4, 12))
			draw_text('' + str(coin), font_coin, white, tile_size - 5, 2)

			for i in range(0 ,player.health+1):
				screen.blit(health_img, (screen_width-(i*30), 10))


		
		enemy1_group.draw(screen, x_modifier)
		lava_group.draw(screen, x_modifier)
		coin_group.draw(screen, x_modifier)
		exit_group.draw(screen, x_modifier)

		
		game_over = player.update(game_over,x_modifier,current_tile_list,screen,group)
		
		#if player has died
		if game_over == -1:
			#pygame.mixer.Sound('img/a.mp3').play()
			draw_text('GAME OVER', font, red, (screen_width // 2) - 240, screen_height // 2 -200)
			if restart_button.draw(screen):
				world_data = []
				world = World(reset_level(level), no_of_tile, tile_size, group)
				game_over = 0
				coin = 0
			if exit_button.draw(screen):
				run = False
		
		#draw_grid()
		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= total_levels:
				#reset level
				world_data = [] 
				world = World(reset_level(level), no_of_tile, tile_size, group)
				game_over = 0
			else:
				if restart_button.draw(screen):
					level = 0
					#reset level
					world_data = []
					world = World(reset_level(level), no_of_tile, tile_size, group)
					game_over = 0
					coin = 0

	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#print(clock.get_fps())
	pygame.display.update()
	clock.tick(FPS)
		
pygame.quit()

