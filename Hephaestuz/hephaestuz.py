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

def update():
    global spawn_timer

    player.move(keyboard)
    spawn_timer -= 1

    if spawn_timer == 0 and len(enemies) < 40:

        spawn_timer = random.choice((120,180,240))
        spawn_pos = ()

        spawn_axi = random.choice((0,1))
        
        if spawn_axi == 0: 
            spawn_pos = (random.choice((-80,WIDTH + 80)), random.randint(-80, HEIGHT + 80))
        elif spawn_axi == 1: 
            spawn_pos = (random.randint(-80,WIDTH + 80), random.choice((-80, HEIGHT + 80)))

        enemies.append(Enemy(spawn_pos))

    for enemy in enemies:
        enemy.follow(player.pos)
        
        if enemy.hitbox().colliderect(player.hitbox()):
             print("O player foi pego!")

def draw():
    screen.fill((30,30,30))
    background.draw()
    player.draw()
    screen.draw.rect(player.hitbox(), 'blue')
    for enemy in enemies:
        enemy.draw()
        screen.draw.rect(enemy.hitbox(), 'red')

pgzrun.go()