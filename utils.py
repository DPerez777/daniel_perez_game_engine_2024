# this code was made made by Mr. Cozort
import pygame as pg

from math import floor

class Timer():
    # set everything to 0 when initiated
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0

    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
    # reset cooldown
    def get_countdown(self):
        return floor(self.cd)
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt
    def event_reset(self):
        self.event_time = floor((pg.time.get_tickets())/1000)
    # set current time
    def event_reset(self):
        self.current_time = floor((pg.time.get_tickets())/1000)