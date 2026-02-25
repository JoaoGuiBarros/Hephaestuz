from pgzero.actor import Actor
from pygame import Rect

from scripts.settings import *

import math
import random

class Player(Actor):

    def __init__(self):

        super().__init__('player_1', (WIDTH // 2,HEIGHT // 2))

        self.speed = 3.5

        self.sprite_animation = [f"player_{i}" for i in range(1,5)]
        self.animation_cycle = 0
        self.hitbox_height = 8
        self.hitbox_width = 6

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

        map_gap = 6 * 4

        if self.hitbox().right > WIDTH - map_gap: self.x = WIDTH - map_gap - self.hitbox_width // 2 * 4
        if self.hitbox().left < map_gap: self.x = map_gap + self.hitbox_width // 2 * 4
        if self.hitbox().bottom > HEIGHT - map_gap: self.y = HEIGHT - map_gap
        if self.hitbox().top < map_gap: self.y = map_gap + self.hitbox_height * 4

    def hitbox(self):
        return Rect(
            self.x - self.hitbox_width // 2 * 4, 
            self.y - self.hitbox_height * 4, 
            self.hitbox_width * 4,
            self.hitbox_height * 4
        )
