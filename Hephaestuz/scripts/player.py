from pgzero.actor import Actor
from pygame import Rect

from scripts.settings import *

import math
import random

class Player(Actor):

    def __init__(self):

        super().__init__('player_idle_1', (WIDTH / 2,HEIGHT // 2))
        
        self.state = "idle"
        self.base_speed = 3.5
        self.speed = 3.5
        self.health = 3
        self.iframes = 0

        self.anchor = ('center','bottom')
        self.hitbox_height = 8
        self.hitbox_width = 6

        self.idle_animation = ["player_idle_1" for i in range(2)] + ["player_idle_2" for i in range(2)]
        self.walking_animation = [f"player_walk_{i}" for i in range(1,5)]
        self.sprite_animation = self.idle_animation
        self.animation_cycle = 0

        self.hitflash = False
        self.has_shadow = True
        
    def move(self, keyboard):

        self.speed += (self.base_speed - self.speed) * .05

        xdir = keyboard.d - keyboard.a 
        ydir = keyboard.s - keyboard.w

        if abs(xdir) or abs(ydir):
             
            magnitude = math.sqrt(xdir**2 + ydir**2)
            
            self.x += (xdir / magnitude) * self.speed
            self.y += (ydir / magnitude) * self.speed

            self.apply_boundaries()

            self.sprite_animation = self.walking_animation

        else: self.sprite_animation = self.idle_animation


    def apply_boundaries(self):

        map_gap = 8

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