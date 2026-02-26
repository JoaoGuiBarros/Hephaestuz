from pgzero.loaders import sounds
from pgzero.actor import Actor
from pygame import Rect

import math

class Snipear(Actor):

    def __init__(self, player):

        super().__init__('snipear_1')

        self.kills = 0
        self.impacts = []
        self.shot_trail = {"init_pos": (0,0), "end_pos": (0,0), "life": 0}
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
        self.shot_attack_speed = 120
        self.shot_cooldown = 0
        self.shot_buffer = 0
        
    def attack(self, is_mute):

        if self.cooldown != 0: return

        if not is_mute: sounds.attack.play()
        self.attack_buffer = 0
        self.cooldown = self.attack_speed
        self.current_gap = 80

    def shot(self, enemies, is_mute):

        if self.shot_cooldown != 0: return
        
        self.shot_buffer = 0
        self.shot_cooldown = self.shot_attack_speed
        self.current_gap = 20
        self.attack_buffer = 0
        self.cooldown = self.attack_speed

        angle_rad = math.radians(-self.angle_store)
    
        gun_tip_distance = 60
        
        shot_x = self.x + math.cos(angle_rad) * gun_tip_distance
        shot_y = self.y + math.sin(angle_rad) * gun_tip_distance
        
        self.shot_trail["init_pos"] = (shot_x, shot_y)
        
        ray_length = 2000
        self.shot_trail["end_pos"] = (
            shot_x + math.cos(angle_rad) * ray_length,
            shot_y + math.sin(angle_rad) * ray_length
        )

        self.shot_trail["life"] = 2
        if not is_mute: sounds.shot.play()

        for i in range(0, ray_length, 10):
    
            check_x = shot_x + math.cos(angle_rad) * i
            check_y = shot_y + math.sin(angle_rad) * i
            
            point = (check_x, check_y)

            for enemy in enemies[:]:

                if enemy.hitbox().collidepoint(point):
                    
                    self.impacts.append({"pos": enemy.topleft, "life": 5})
                    enemies.remove(enemy)

                    if self.sound_allowed:
                        self.sound_allowed = False
                        if not is_mute: sounds.player_hit.play()

                    self.kills += .5

    def update(self, mouse_pos, enemies, is_mute):

        self.cooldown = max(self.cooldown - 1, 0)
        self.shot_cooldown = max(self.shot_cooldown - 1, 0)

        if self.shot_buffer != 0: self.shot(enemies, is_mute)
        elif self.attack_buffer != 0: self.attack(is_mute)

        self.attack_buffer = max(self.attack_buffer - 1, 0)
        self.shot_buffer = max(self.shot_buffer - 1, 0)

        ox, oy = self.player.x, self.player.y - 24
        dx = mouse_pos[0] - ox
        dy = mouse_pos[1] - oy
        angle_rad = math.atan2(dy, dx)
        self.angle = math.degrees(-angle_rad)
        self.angle_store = self.angle

        self.current_gap += (self.base_gap - self.current_gap) * self.return_speed
        
        self.x = ox + math.cos(angle_rad) * self.current_gap
        self.y = oy + math.sin(angle_rad) * self.current_gap

        if self.cooldown > (self.attack_speed - 2): 
            self.check_collisions(enemies, is_mute)
            self.image = self.atk_sprite
            self.angle = self.angle_store
        else:
            self.image = self.rest_sprite
            self.angle = self.angle_store
            self.sound_allowed = True  

    def check_collisions(self, enemies, is_mute):
     
        num_points = 7
        spacing = 16

        for i in range(num_points):

            angle_rad = math.radians(-self.angle_store)
            
            check_x = self.x + math.cos(angle_rad) * (i * spacing)
            check_y = self.y + math.sin(angle_rad) * (i * spacing)

            hitbox_size = 40

            temp_rect = Rect(
                check_x - hitbox_size // 2, 
                check_y - hitbox_size // 2, 
                hitbox_size, 
                hitbox_size
            ) 

            for enemy in enemies[:]:

                if temp_rect.colliderect(enemy.hitbox()):

                    self.impacts.append({"pos":(enemy.topleft), "life": 2})
                    enemies.remove(enemy)

                    self.kills += 1

                    if self.sound_allowed:
                        self.sound_allowed = False
                        if not is_mute: sounds.player_hit.play()