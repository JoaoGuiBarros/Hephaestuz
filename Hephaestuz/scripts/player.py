from pgzero.actor import Actor
from pygame import Rect

from scripts.settings import *

import math
import random

class Player(Actor):

    def __init__(self):

        super().__init__('player', (WIDTH // 2,HEIGHT // 2))
        self.speed = 3.5

        self.height = 12
        self.width = 8

        self.anchor = ('center','bottom')
        
    def move(self, keyboard):

        xdir = (keyboard.d or keyboard.right) - (keyboard.a or keyboard.left)
        ydir = (keyboard.s or keyboard.down) - (keyboard.w or keyboard.up)

        if abs(xdir) or abs(ydir):
             
            magnitude = math.sqrt(xdir**2 + ydir**2)
            
            self.x += (xdir / magnitude) * self.speed
            self.y += (ydir / magnitude) * self.speed

            self.apply_boundaries()

    def apply_boundaries(self):
        if self.hitbox().right > WIDTH - 6 * 4: self.x = WIDTH - 6 * 4 - (self.width // 2 * 4)
        if self.hitbox().left < 6 * 4: self.x = 6 * 4 + (self.width // 2 * 4)
        if self.hitbox().bottom > HEIGHT - 24: self.y = HEIGHT - 24
        if self.hitbox().top < 24: self.y = 24 + (self.height * 4)
        

    def hitbox(self):
        return Rect(
            self.x - (self.width // 2 * 4), 
            self.y - self.height * 4,
            self.width * 4,
            self.height * 4,
        )
