from pgzero.loaders import sounds
from pgzero.actor import Actor
from pygame import Rect

import math

class Snipear(Actor):

    def __init__(self, player):

        super().__init__('snipear_1')
        self.kills = 0
        self.impacts = []
        self.pos = (-100, -100)
        self.has_shadow = False
        self.speed = 3.5
        self.animation_cycle = -1
        self.hitbox_height = 8
        self.hitbox_width = 6
        self.sound_allowed = True
        self.sound_trigger = False
        self.atk_sprite = 'snipear_2'
        self.rest_sprite = 'snipear_1'
        self.angle_store = 0
        self.player = player
        self.anchor = ('left','center')
        self.base_gap = 32   
        self.current_gap = 32  
        self.attack_buffer = 0
        self.attack_speed = 50
        self.cooldown = 0
        self.return_speed = 0.075
        
    def attack(self, is_mute):
        if self.cooldown == 0:
            if not is_mute: sounds.attack.play()
            self.attack_buffer = 0
            self.cooldown = self.attack_speed
            self.current_gap = 80

    def hitbox(self):

        return Rect(self.x - 16, self.y - 16, 32, 32) 

    def update(self, mouse_pos, enemies, is_mute):

        self.cooldown = max(self.cooldown - 1, 0)

        if self.attack_buffer != 0:
            self.attack(is_mute)

        self.attack_buffer = max(self.attack_buffer - 1, 0)

        ox, oy = self.player.x, self.player.y - 24
        dx = mouse_pos[0] - ox
        dy = mouse_pos[1] - oy
        angle_rad = math.atan2(dy, dx)
        self.angle = math.degrees(-angle_rad)
        self.angle_store = self.angle

        self.current_gap += (self.base_gap - self.current_gap) * self.return_speed
        
        self.x = ox + math.cos(angle_rad) * self.current_gap
        self.y = oy + math.sin(angle_rad) * self.current_gap

        if self.cooldown > (self.attack_speed // 1.15): 
            self.check_collisions(enemies)
            self.image = self.atk_sprite
            self.angle = self.angle_store
        else:
            self.image = self.rest_sprite
            self.angle = self.angle_store
            self.sound_allowed = True
        

    def check_collisions(self, enemies):
     
        num_points = 16

        spacing = 6

        for i in range(num_points):

            angle_rad = math.radians(-self.angle)
        
            check_x = self.x + math.cos(angle_rad) * (i * spacing)
            check_y = self.y + math.sin(angle_rad) * (i * spacing)

            temp_rect = Rect(check_x - 4, check_y - 4, 40, 40)

            for enemy in enemies[:]:
                if temp_rect.colliderect(enemy.hitbox()):
                    self.impacts.append((enemy.topleft))
                    enemies.remove(enemy)
                    self.kills += 1
                    if self.sound_allowed:
                        self.sound_allowed = False
                        self.sound_trigger = True
                        

        
                    