# This file was created by: Daniel Perez
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice
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
        self.image.fill(GREEN)
        # makes the rectangular area of the plane
        self.rect = self.image.get_rect()
        # sets the x and y positions for the player
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 100
        self.cooling = False
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

    # will move the player around the screen (incomplete)
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy

    # prevent player from going in walls
    # def collide_with_walls(self, dx=0, dy=0):
    #     # make for loop using self.game.walls
    #     for wall in self.game.walls:
    #         # if the x/y value of the wall equals the player's x/y value + the movement event, collide_with_walls = True, else False
    #         if wall.x == self.x +dx and wall.y == self.y + dy:
    #             return True
    #     return False
    # will update the game so that the player's position is constantly updated?
    
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
        # check if player y = wall = 
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
                self.moneybag += 1
                hits[0].kill()
            if str(hits[0].__class__.__name__) == "PowerUp":
                if self.hitpoints < 100:
                    self.hitpoints += 1
                    hits[0].kill()
                # self.speed += 200
                
            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                self.hitpoints -= 1
                # print(self.hitpoints)
                if self.timer.get_countdown() > 15:
                    self.hitpoints -= 1
            



    
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
        self.collide_with_group(self.game.coins, True)
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
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
        self.timer = Timer(self.game)
    
    def update(self):
        if self.timer.get_countdown() == 15:
            self.image.fill(BLACK)

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


class PowerUp(pg.sprite.Sprite):
    # initialize the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set game class
        self.game = game
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
        self.timer = Timer(self.game)
    # can't pass through walls 
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
    # make Mob follow player (?)d
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

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
        if self.timer.get_current_time() == 14:
            self.image = pg.surface.Surface((TILESIZE*1.5,TILESIZE*1.5))
            self.speed = 110
        if self.timer.get_current_time() >= 15:
            self.image = pg.surface.Surface((TILESIZE*2,TILESIZE*2))
            self.speed = 135
        


    # def collide_with_group(self, group):
    #     hits = pg.sprite.spritecollide(self, group, kill)
    #     if hits: return True

    # def collide_with_powerups(self, dir):
    #     if dir == 'x':
    #         hits = pg.sprite.spritecollide(self, self.game.powerups, True)
    #         if hits:
    #             if self.vx > 0:
    #                 self.x = hits[0].rect.left - self.rect.width
    #             if self.vx < 0:
    #                 self.x = hits[0].rect.right
    #             self.vx = 0
    #             self.rect.x = self.x
    #             if hits:
    #                 return
    #     if dir == 'y':
    #         hits = pg.sprite.spritecollide(self, self.game.powerups, True)
    #         if hits:
    #             if self.vy > 0:
    #                 self.y = hits[0].rect.top - self.rect.height
    #             if self.vy < 0:
    #                 self.y = hits[0].rect.bottom
    #             self.vy = 0
    #             self.rect.y = self.y

# # sets the name of p1
# p1 = Player("Belda")
# # prints the name of p1
# print(p1.name)