# This file was created by: Daniel Perez
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice


from os import path
from pygame.sprite import Sprite

SPRITESHEET = "theBell.png"

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1.5, height * 1.5))
        return image
# ^ allows us to import/use pygame and imports all settings from settings

# make player class, subclass of pg.sprite.Sprite
class Player(pg.sprite.Sprite):
    # initialize the player class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set game class
        self.game = game
        # makes dimensions for the player image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # fills self.image with color (GREEN), defined in settings
        self.spritesheet = Spritesheet(path.join(img_dir, 'theBell.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        # makes the rectangular area of the plane
        self.rect = self.image.get_rect()
        # sets the x and y positions for the player
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 50
        self.powerup_cooling = False
        self.coin_cooling = False
        self.timer = Timer(self.game)
    
    # make the player follow WASD or the arrows 
    def get_keys(self):
        self.vs, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_t]:
            self.game.test_timer.event_reset()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    
    # stop player movement when colliding with walls
    def collide_with_walls(self, dir):
        # check if player x = wall x
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        # check if player y = wall 
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    # made possible by Aayush's question!
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                if hits[0].collectable:
                    self.moneybag += 1
                    hits[0].collectable = False
                # hits[0].kill()
            if str(hits[0].__class__.__name__) == "PowerUp":
                if self.hitpoints < 50 and self.powerup_cooling == False:
                    self.hitpoints += 5
                    self.game.cooldown.cd = 5
                    self.powerup_cooling = True
                # self.speed += 200
                if self.timer.get_countdown() >= self.timer.get_countdown() + 5 and self.powerup_cooling == True:
                    self.powerup_cooling = False
                
            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                self.hitpoints -= 1
                # print(self.hitpoints)
                if self.timer.get_countdown() > 15:
                    self.hitpoints -= 1
            
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom


    
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later           
        self.collide_with_walls('y')
                    
        self.collide_with_group(self.game.coins, False)
        if self.game.cooldown.cd < 1:
            self.cooling = False
        # if not self.cooling:
        #     self.game.powerup_respawn = True
        # make power_ups and mobs False when colliding
        self.collide_with_group(self.game.power_ups, False)
        self.collide_with_group(self.game.mobs, False)
        
        



# creates the "Wall" class, subclass of pg.sprite.Sprite
class Wall(pg.sprite.Sprite):
    # initialize the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set game class
        self.game = game
        # sets the dimensions for the wall image
        self.image = pg.Surface((TILESIZE, TILESIZE))    
        # sets the color for the wall
        self.image.fill(BROWN)
        # makes the rectangular area of the wall
        self.rect = self.image.get_rect()
        # sets the coordinates of the wall
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def update(self):
        if self.game.timer.get_current_time() >= 15:
            self.image.fill(WALL2)

# Coin sprites
class Coin(pg.sprite.Sprite):
    # initialize the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set game class
        self.game = game
        # sets the dimensions for the wall image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # sets the color for the coin
        self.image.fill(YELLOW)
        # makes the rectangular area of the coin
        self.rect = self.image.get_rect()
        # sets the coordinates of the wall
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.cooldown = 5
        self.timer = self.cooldown
        self.collectable = False

    # made possible by Ayuush
    def update(self):
        self.image.fill(ORANGE)
        if self.collectable == False:
            self.timer -= self.game.dt
            if self.timer <= 0:
                self.collectable = True
                self.timer = self.cooldown
    
        


class PowerUp(pg.sprite.Sprite):
    # initialize the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set game class
        self.game = game
        # self.respawn = 
        # sets the dimensions for the wall image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # sets the color for the coin
        self.image.fill(BLUE)
        # makes the rectangular area of the coin
        self.rect = self.image.get_rect()
        # sets the coordinates of the wall
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def update(self):
        if self.game.timer.get_current_time() >= 15:
            self.image.fill(CYAN)
    
    # def 

# creates the class "Mob"
class Mob(pg.sprite.Sprite):
    
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set set self.game to game
        self.game = game
        # set dimensions for the image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # set mob color to RED
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # set coords of Mob
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 90
        self.health = 1000
    # can't pass through walls (it can now pass through walls as a feature)
    def collide_with_walls(self, dir):
        # check if x coord is the same as wall x coord
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # return to original position if interact with wall
                # doesn't this method allow for glitches if spammed enough?
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        # check if y coord is the same as wall y coord
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            # return to original position if interact with wall
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Player":
                self.vx *= -1
                self.vy *= -1
    # make Mob follow player (?)d
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # move the mob
        if self.rect.x < self.game.player.rect.x:
            self.vx = self.speed
        if self.rect.x > self.game.player.rect.x:
            self.vx = -self.speed 
        if self.rect.y < self.game.player.rect.y:
            self.vy = self.speed
        if self.rect.y > self.game.player.rect.y:
            self.vy = -self.speed
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')
        # transform the mob after 14s
        if self.game.timer.get_current_time() == 14:
            self.image = pg.surface.Surface((TILESIZE*1.5,TILESIZE*1.5))
            self.speed = 110
        if self.game.timer.get_current_time() >= 15:
            self.image = pg.surface.Surface((TILESIZE*2,TILESIZE*2))
            self.speed = 135
        if self.game.timer.get_current_time() >= 30:
            self.speed = 165
        if self.game.timer.get_current_time() >= 50:
            self.speed = 190





