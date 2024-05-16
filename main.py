# This file was created by: Daniel Perez
# testing github commiting system
# imports pygame as well as the width, height, and title of the game
import pygame as pg
from settings import *
# the asterix above  ^ means that it imports everything from the file
# this imports randint from random
from random import randint
# import all from sprites
from sprites import *
from utils import *
# import module for variables
import sys
# import path from os
from os import path
# import rounding for the clock
from math import floor

'''
menu screen - player chooses when to start the game, but must press button to do so DONE
feedback when player gets hurt - shows player they took damage, DONE
make levels (make a final boss) DONE
respawn powerups and coins DONE
make death screen/end game if hp=0 DONE
make boss harder and have final objective DONE
economy DONE
shop ONGOING
'''


# creates the game blueprint
class Game:
    # Initializer -- initializes information about the game
    def __init__(self):
        # initializes pygame
        pg.init()
        # settings 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting up the pygame clock
        self.clock = pg.time.Clock()
        self.timer = Timer(self)
        # speed boost timer from ChatGPT
        self.speed_boost_duration = 3
        self.speed_boost_timer = 0
        self.speed_boost_activate = False
        keys = pg.key.get_pressed()
    # gonna load data to the RAM
    def load_data(self):
        # make game_folder var for the file path 
        game_folder = path.dirname(__file__)
        # make self.map_data a list
        self.map_data = []
        '''
        The with statement is a context manager in Python.
        It is used to ensure that a resource is properly closed or released
        after it is used. This can help to prevent errors and leaks.
        - Mr. Cozort
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                # print each line in f
                print(line)
                # put each line in f into the self.map_data list
                self.map_data.append(line)

     # Create run method which runs the whole GAME
    def new(self):
        self.load_data()
        # make the timer
        self.cooldown = Timer(self)
        # make text saying "create new game..."
        print("create new game...")
        # define multiple self.x var
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shop = pg.sprite.Group()
        
        # make a for loop from self.map_data list
        for row, tiles in enumerate(self.map_data):
            print(row)
            # make a for loop from row
            for col, tile in enumerate(tiles):
                print(col)
                # if tile has a value of '1', print a wall at said tile
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                # if tile has a vlue of 'P', there is a player at said tile
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'S':
                    Shop(self, col, row)

    # Runs the game
    def run(self):
        self.playing = True
        while self.playing and self.player.hitpoints > 0:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        else:
            self.quit()
    def quit(self):
        pg.quit()
        sys.exit()

    
    
    # draw the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # allow text to appear with font, color, etc
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

    # show text and bg color
    def draw(self):
        # change bg color after 15s
        if self.timer.get_current_time() >= 15:
            self.screen.fill(BGCOLOR2)
        else: self.screen.fill(BGCOLOR)
        
        # display notifications
        self.all_sprites.draw(self.screen)
        if self.timer.get_current_time() == 7:
            self.draw_text(self.screen, "spawning...", 24, YELLOW, 70, 70)
        if self.timer.get_current_time() == 7:
            self.draw_text(self.screen, "spawning...", 24, YELLOW, 865, 615)
        if self.timer.get_current_time() == 3:
            self.draw_text(self.screen, "Coins Spawn in 3", 24, ORANGE, 440, 30)
        if self.timer.get_current_time() == 4:
            self.draw_text(self.screen, "Coins Spawn in 2", 24, ORANGE, 440, 30)
        if self.timer.get_current_time() == 5:
            self.draw_text(self.screen, "Coins Spawn in 1", 24, ORANGE, 440, 30)
        if self.timer.get_current_time() == 50:
            self.draw_text(self.screen, "10 Seconds left", 60, RED, 350, HEIGHT/2 - 100)
        if self.timer.get_current_time() == 51:
            self.draw_text(self.screen, "10 Seconds left", 60, RED, 350, HEIGHT/2 - 100)
        if self.timer.get_current_time() == 57:
            self.draw_text(self.screen, "3 Seconds left", 60, RED, 350, HEIGHT/2 - 100)
        if self.timer.get_current_time() == 58:
            self.draw_text(self.screen, "2 Seconds left", 60, RED, 350, HEIGHT/2 - 100)
        if self.timer.get_current_time() == 59:
            self.draw_text(self.screen, "1 Seconds left", 60, RED, 350, HEIGHT/2 - 100)
        
        if self.timer.get_current_time() == 14:
            self.draw_text(self.screen, "BOSS SPAWNING!!!", 59, RED, 289, HEIGHT/2 - 150)
        
        # make the text change color after 15s
        if self.timer.get_current_time() >= 15:
            self.draw_text(self.screen, str(self.player.moneybag), 32, ORANGE, 1, 0)
            self.draw_text(self.screen, "HP " + str(self.player.hitpoints), 32, CYAN, 935, 0)
            self.draw_text(self.screen, "Level 2", 32, WHITE, WIDTH/4, 1)
            if len(self.player.inventory) >= 1:
                self.draw_text(self.screen, "Speed Boost (Spam P)", 32, YELLOW, 720, 730)
        else:
            self.draw_text(self.screen, str(self.player.moneybag), 32, YELLOW, 1, 0)
            self.draw_text(self.screen, "HP " + str(self.player.hitpoints), 32, BLUE, 935, 0)
            self.draw_text(self.screen, "Level 1", 32, BLACK, WIDTH/4 - 32, 1)
            if len(self.player.inventory) >= 1:
                self.draw_text(self.screen, "Speed Boost (Spam P)", 32, YELLOW, 720, 730)
        
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            # if the quit event occurs, quit self
            if event.type == pg.QUIT:
                self.quit()
    
    # start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Survive 60 seconds to Win!", 24, GREEN, WIDTH/2.5, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_win_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You Win!", 24, GREEN, WIDTH/2.5, HEIGHT/2)
        pg.display.flip()

    # wait for KEYUP to start
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def update(self):
        # make the test timer tick
        self.cooldown.ticking()
        self.all_sprites.update()
        # the following was inspired by ChatGPT
        collisions = pg.sprite.spritecollide(self.player, self.shop, False)
        for shop_collision in collisions:
            # check to see if player has less than 5 boosts
            if len(self.player.inventory) <= 5:
                # Check if player has at least 5 coins
                if self.player.moneybag >= 5:
                    # Remove 5 coins from the player's inventory
                    self.player.moneybag -= 5
                    # Give the player the speed item
                    self.player.inventory['speed'] = True                 

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    # print("great")
                    if "speed" in self.player.inventory and not self.speed_boost_activate:
                        self.player.speed += 200
                        self.speed_boost_activate = True
                        # print("vrooom")
                        # set the duration for the speed boost
                        self.speed_boost_timer = self.speed_boost_duration

        

        # Decrease the speed boost timer
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= self.dt
            # Check if the speed boost timer has expired
            if self.speed_boost_timer <= 0:
                # Reset player speed and remove "speed" from inventory
                self.player.speed = PLAYER_SPEED
                del self.player.inventory["speed"]
                # print(self.player.speed)
                self.speed_boost_activate = False

            
        if self.timer.get_current_time() >= 60:
            self.show_win_screen()
        if self.timer.get_current_time() >= 61:
            self.quit()

    


# Create a new game
g = Game()
# use new game method to run
# g.show_start_screen()
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()