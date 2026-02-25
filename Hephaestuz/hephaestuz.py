import pgzrun
from pygame import Rect

from scripts.settings import *
from scripts.player import Player
from scripts.enemy import Enemy

import math
import random

background = Actor('background')
player = Player()

enemies = []

spawn_timer = random.choice((120,180,240))

def spawn_manager():

    global spawn_timer

    if spawn_timer == 0 and len(enemies) < 40:

            spawn_timer = random.choice((120,180,240))
            spawn_pos = ()

            spawn_axi = random.choice((0,1))
            
            if spawn_axi == 0: 
                spawn_pos = (random.choice((-80,WIDTH + 80)), random.randint(-80, HEIGHT + 80))
            elif spawn_axi == 1: 
                spawn_pos = (random.randint(-80,WIDTH + 80), random.choice((-80, HEIGHT + 80)))

            enemies.append(Enemy(spawn_pos))

def enemy_manager():

    spawn_manager()

    for enemy in enemies:

            enemy.follow(player.pos)

            for other in enemies:

                if enemy != other:
                
                    dist = math.sqrt((enemy.x - other.x)**2 + (enemy.y - other.y)**2)
                    
                    if dist < 40:
                    
                        if dist == 0: dist = 1 
                        enemy.x -= (other.x - enemy.x) / dist * 0.5
                        enemy.y -= (other.y - enemy.y) / dist * 0.5

            if enemy.hitbox().colliderect(player.hitbox()):

                print("XX")

def update():

    global spawn_timer

    player.move(keyboard)
    spawn_timer -= 1

    enemy_manager()

def animate(obj): 
    obj.animation_cycle += .1
    obj.animation_cycle = obj.animation_cycle % len(obj.sprite_animation)
    obj.image = obj.sprite_animation[math.floor(obj.animation_cycle)]

def draw():

    background.draw()

    render_list = [player] + enemies
    render_list.sort(key=lambda obj: obj.y)
    
    for obj in render_list: 
        screen.draw.filled_rect(Rect(
            obj.left + 4,
            obj.y - 4,
            obj.width - 8,
            4
        ), (89,86,82))
        animate(obj)
        obj.draw() 

pgzrun.go()