### Importing Pgzero (and Rect from pygame) ###
import pgzrun
from pygame import Rect

### Importing scripts ###
from scripts.settings import *
from scripts.player import Player

### Importing extra libs ###
import math
import random

background = Actor('background')
player = Player()

def update():
    player.move(keyboard)

def draw():
    screen.fill((30,30,30))
    background.draw()
    player.draw()

pgzrun.go()