from pgzero.actor import Actor
from pygame import Rect

import math

class Enemy(Actor):
    
    def __init__(self, pos):

        super().__init__('enemy', pos)

        self.speed = 1.5

        self.height = 14
        self.width = 8

        self.anchor = ('center','bottom')

    def follow(self, target_pos):

        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def hitbox(self):

        return Rect(
            self.x - (self.width // 2 * 4), 
            self.y - self.height * 4,
            self.width * 4,
            self.height * 4,
        )
