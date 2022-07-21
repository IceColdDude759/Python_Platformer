import pygame
from spritesheetparser import Spritesheet
from tiles import *
from camera import *
from Player import *
from menu import *



class Engine():
	def __init__(self):
		
		pygame.init()
		#pygame.mixer.pre_init(44100, -16, 2, 512)
		#mixer.init()
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.running = True
		self.menu_bol = False
		self.screen_width, self.screen_height = 800, 480
		self.tile_size = 32
		self.flags = pygame.RESIZABLE | pygame.SCALED
		
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), self.flags)
		self.title = "Ani GAME"
		pygame.display.set_caption(self.title)

		
		self.level = 1
		self.dt = 0
		self.menu = True
		self.health = 3
		self.coin = 0
		self.tick = 0
		
		self.reset_level(self.level, True)
		
		
		self.init_menu()
		self.init_keys()
		self.load()


	def load(self):
		#load images
		self.health_img = pygame.image.load('img/heart.png')
		self.health_img = pygame.transform.scale(self.health_img,(30,30))
		self.coin_img = pygame.image.load('img/coin.png')
		self.coin_img = pygame.transform.scale(self.coin_img,(20,20))
		self.bg_img = pygame.image.load('resources/back.png').convert()
		self.bg_img = pygame.transform.scale(self.bg_img, (self.screen_width, self.screen_height-self.tile_size*0))
		self.restart_img = pygame.image.load('img/button/Restart.png')
		self.restart_img = pygame.transform.scale(self.restart_img,(80,80))
		self.start_img = pygame.image.load('img/button/Start.png')
		self.start_img = pygame.transform.scale(self.start_img,(200,100))
		self.exit_img = pygame.image.load('img/button/Exit.png')
		self.exit_img = pygame.transform.scale(self.exit_img,(200,100))

		self.font_coin = pygame.font.SysFont("Verdana", 30)



	def reset_level(self, level, alive):
		if not(alive) :
			self.coin = 0
			self.health = self.health
			
		self.game_state = 0
		self.enemy_group = ModifiedGroup(self)
		self.coin_group = ModifiedGroup(self)
		self.lava_group = ModifiedGroup(self)
		self.exit_group = ModifiedGroup(self)

		self.main_tiles = Spritesheet('resources/Blockz')
		self.world = TileMap(f'map{level}.csv', self.main_tiles, self)
		self.tiles = self.world.tiles
		self.left_border = 0
		self.top_border = 0
		self.bottom_border = self.world.map_h
		self.right_border = self.world.map_w

		self.player = Player(self)
		self.camera = Camera(self)
		self.follow = Follow(self)
		self.border = Border(self)
		self.auto = Auto(self)
		self.camera.setmethod(self.border)
		
		
	
	def init_menu(self):
		self.mainmenu = Mainmenu(self)
		self.deadmenu = Deadmenu(self)

	
	def init_keys (self):
		self.LEFT_KEY, self.RIGHT_KEY = False, False
		self.UP_KEY, self.DOWN_KEY = False, False
		self.SPACE_KEY = False


	def input(self):
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.running = False

				## PROCESS KEYPRESS
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.LEFT_KEY = True
				elif event.key == pygame.K_RIGHT:
					self.RIGHT_KEY = True
				elif event.key == pygame.K_UP:
					self.UP_KEY = True
				elif event.key == pygame.K_DOWN:
					self.DOWN_KEY = True
				elif event.key == pygame.K_SPACE:
					self.SPACE_KEY = True

				## HANDEL CAMERA MOVEMENT	
				elif event.key == pygame.K_1:
					self.camera.setmethod(self.follow)
				elif event.key == pygame.K_2:
					self.camera.setmethod(self.auto)
				elif event.key == pygame.K_3:
					self.camera.setmethod(self.border)

				elif event.key == pygame.K_ESCAPE:
					self.running = False

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					self.LEFT_KEY = False
				elif event.key == pygame.K_RIGHT:
					self.RIGHT_KEY = False
				elif event.key == pygame.K_UP:
					self.UP_KEY = False
				elif event.key == pygame.K_DOWN:
					self.DOWN_KEY = False
				elif event.key == pygame.K_SPACE:
					self.SPACE_KEY = False


	def update(self):
		
		self.dt = self.clock.tick(60) * .001 * self.FPS 
		self.tick = self.clock.get_time()
		#print(self.clock.tick(60))
		self.player.update()
		self.camera.scroll()
		self.enemy_group.update(self.tick)
		self.lava_group.update(self.tick)


	def draw(self):
		self.screen.blit(self.bg_img, (0, 0))
		self.world.draw_world()
		self.enemy_group.draw()
		self.lava_group.draw()
		self.coin_group.draw()
		self.exit_group.draw()
		self.player.draw()
		self.draw_hud()

		
		#pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 2)
		

	def draw_text(self,text, font, colour, x, y):
		img = font.render(text, True, colour)
		self.screen.blit(img, (x, y))


	def draw_hud(self):
		self.screen.blit(self.coin_img, (4, 10))
		self.draw_text('' + str(self.player.coin), self.font_coin, (255,255,255), self.tile_size - 5, 0)
		for i in range(0 ,self.player.health):
			self.screen.blit(self.health_img, (self.screen_width-(35+(i*30)), 4))


	def mainloop(self):

		self.input()

		if self.menu:
			self.mainmenu.draw()
			if self.mainmenu.buttons['Exit'][1]:
				self.running = False
			if self.mainmenu.buttons['Start'][1]:
				self.menu = False
			
		else :
			self.draw()

			if self.game_state == 0:
				self.update()
				self.draw_hud()

			elif self.game_state == -1:
				self.screen.fill((0,0,0))
				self.player.draw()
				self.deadmenu.draw()
				if self.deadmenu.buttons['Exit'][1]:
					self.running = False
				if self.deadmenu.buttons['Restart'][1]:
					self.reset_level(self.level, False)
				
			
			elif self.game_state == 1:
				self.coin = self.player.coin
				self.health = self.player.health
				self.level += 1
				if self.level > 2:
					self.level = 1
					self.menu=True
					self.screen.blit(self.bg_img, (0, 0))
				else:
					self.reset_level(self.level,True)

		pygame.display.update()


if __name__ == "__main__":
	engine = Engine()
	while engine.running :
		engine.mainloop()
		