from pgzero.actor import Actor
from pygame import Rect

import math
import random

class Enemy(Actor):

    def __init__(self, pos):

        super().__init__('enemy_1', pos)

        self.speed = random.choice((1.5, 2, 2.5))

        self.sprite_animation = [f"enemy_{i}" for i in range(1,5)]
        self.animation_cycle = 0
        self.has_shadow = True

        self.anchor = ('center','bottom')
        self.hitbox_height = 12
        self.hitbox_width = 12
        

    def follow(self, target_pos):
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0 and distance > self.speed:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def hitbox(self):
        return Rect(
            self.x - (self.hitbox_width // 2 * 4), 
            self.y - self.hitbox_height * 4,
            self.hitbox_width * 4,
            self.hitbox_height * 4,
        )