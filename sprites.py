# This file was created by: Daniel Perez
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
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

    def get_keys(self):
        self.vs, self.vy = 0, 0
        keys = pg.key.get_pressed()
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
        
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    
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
        if self.collide_with_group(self.game.powerups, True):
            self.moneybag += 1



# creates the "Wall" class, subclass of pg.sprite.Sprite
class Wall(pg.sprite.Sprite):
    # initialize the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        # sets the dimensions for the wall image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # set game class
        self.game = game
        # sets the color for the wall
        self.image.fill(BROWN)
        # makes the rectangular area of the wall
        self.rect = self.image.get_rect()
        # sets the coordinates of the wall
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Coin sprites
class Coin(pg.sprite.Sprite):
    # initialize the wall class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerups
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets the dimensions for the wall image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # set game class
        self.game = game
        # sets the color for the coin
        self.image.fill(YELLOW)
        # makes the rectangular area of the coin
        self.rect = self.image.get_rect()
        # sets the coordinates of the wall
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def collide_with_group(self, group):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: return True

    def collide_with_powerups(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.powerups, True)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
                if hits:
                    return
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.powerups, True)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

# # sets the name of p1
# p1 = Player("Belda")
# # prints the name of p1
# print(p1.name)