import pgzrun
from pygame import Rect

from scripts.settings import *
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.snipear import Snipear

import math
import random

music_vol = 0
is_mute = False

background = Actor('background')

game_timer = 0
game_state = "menu_state"

is_paused = True
hitstop = 0

player = Player()
snipear = Snipear(player)
mouse_pos = (0, 0)

enemies = []
spawn_timer = random.choice((20,40,60))

def spawn_manager():

    global spawn_timer, game_timer

    spawn_timer -= 1

    if spawn_timer <= 0 and len(enemies) < 25:

            spawn_timer = random.choice((0,30,60,90,120) )- min(game_timer // 150, 60)
            spawn_pos = ()

            spawn_axi = random.choice((0,1))
            
            if spawn_axi == 0: 
                spawn_pos = (random.choice((-80,WIDTH + 80)), random.randint(-80, HEIGHT + 80))
            elif spawn_axi == 1: 
                spawn_pos = (random.randint(-80,WIDTH + 80), random.choice((-80, HEIGHT + 80)))

            enemies.append(Enemy(spawn_pos))

def enemy_manager():

    global hitstop, music_vol

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

            if enemy.hitbox().colliderect(player.hitbox()) and player.iframes == 0: 

                if not is_mute: sounds.player_hurt.play()
                snipear.impacts.append(player.topleft)
                player.iframes = 120
                player.health -= 1
                music_vol = 0
                hitstop = 15

def on_mouse_move(pos):

    global mouse_pos
    mouse_pos = pos

def on_mouse_down(button):

    global is_paused, game_state
    if button == mouse.LEFT and not is_paused: snipear.attack_buffer = 10

def update():

    global spawn_timer, game_timer, game_state, is_paused, hitstop, music_vol, is_mute

    if is_mute:
        music_vol = 0
        snipear.sound_trigger = False


    if game_state == "play_state":

        if hitstop != 0: is_paused = True
        else: is_paused = False

    if is_paused: music_vol = 0

    music.set_volume(music_vol)
    if not is_mute: music_vol += (.75 - music_vol) * .01

    hitstop = max(hitstop - 1, 0)

    if is_paused: 
        return

    game_timer += 1

    player.move(keyboard)
    player.iframes = max(player.iframes - 1, 0)
    if player.iframes % 3 == 0: player.hitflash = not player.hitflash
    if player.iframes == 0: player.hitflash = False

    enemy_manager()

    if player.health == 0:
        is_paused = True
        game_state = "restart_state"

    snipear.update(mouse_pos, enemies, is_mute)
    if snipear.sound_trigger and not is_mute:
        sounds.player_hit.play()
        snipear.sound_trigger = False

def animate(obj): 
    if obj.animation_cycle == -1: return 
    obj.animation_cycle += .1
    obj.animation_cycle = obj.animation_cycle % len(obj.sprite_animation)
    obj.image = obj.sprite_animation[math.floor(obj.animation_cycle)]

def draw():

    global game_state

    background.draw()

    if game_state == "menu_state":
        screen.draw.text(
            "HEPHAESTUZ",
            center=(WIDTH // 2, HEIGHT // 2 - 50), 
            fontsize=120, 
            fontname=FONT,
            color="white",
            shadow=(1, 1)
        )

    render_list = [player, snipear] + enemies
    render_list.sort(key=lambda obj: obj.y)

    for obj in render_list:
        if obj.has_shadow:
            screen.draw.filled_rect(Rect(
                obj.left + 4,
                obj.y - 4,
                obj.width - 8,
                4
            ), (89,86,82))
        if not is_paused: animate(obj)
        if getattr(obj, 'hitflash', False): continue
        obj.draw() 

    if len(snipear.impacts) > 0:
        for impact in snipear.impacts:
            screen.blit('impact', impact)
            if hitstop == 0: snipear.impacts.remove(impact)

    if game_state == "play_state":

        screen.draw.text(
            "ENTER to Start or Restart || ESC to return to Menu or Quit || M to Mute and Demute || AWSD to Move || RIGHT-CLICK to Attack", 
            center=(WIDTH // 2, HEIGHT - 10), 
            fontsize=20, 
            fontname=FONT,
            color="white",
            shadow=(1, 1)
        )

    if game_state == "restart_state":
        screen.fill((0,0,0))
        screen.draw.text(
            "GAME OVER", 
            center=(WIDTH // 2, HEIGHT // 2 - 50), 
            fontsize=120, 
            fontname=FONT,
            color="white",
            shadow=(1, 1)
        )

    if is_paused and not game_state == "play_state":
        screen.draw.text(
            "START [ENTER]" if game_state == "menu_state" else "RESTART [ENTER]", 
            center=(WIDTH // 2, HEIGHT // 2 + 80), 
            fontsize=35, 
            fontname=FONT,
            color="white",
            shadow=(2, 2)
        )
        screen.draw.text(
            "MUTE [M]", 
            center=(WIDTH // 2, HEIGHT // 2 + 120), 
            fontsize=35, 
            fontname=FONT,
            color="white",
            shadow=(2, 2)
        )
        screen.draw.text(
            "QUIT [ESC]", 
            center=(WIDTH // 2, HEIGHT // 2 + 160), 
            fontsize=35, 
            fontname=FONT,
            color="white",
            shadow=(2, 2)
        )


def on_key_down(key):
    global spawn_timer, game_timer, game_state, is_paused, hitstop, enemies, is_mute

    if key == keys.RETURN and (game_state == "restart_state" or game_state == "menu_state"):
        if not is_mute: sounds.interact.play()
        music.play('bgm')
        music_vol = 0
        is_paused = False

        if game_state == "restart_state":
            enemies = []
            player.anchor = ('center', 'center')
            player.pos = (WIDTH // 2, HEIGHT // 2)
            player.anchor = ('center','bottom')
            player.health = 3
            player.iframes = 0
            snipear.current_gap = snipear.base_gap
            player.sprite_animation = player.idle_animation
            player.image = player.sprite_animation[0]
            player.hitstop = 0
            snipear.attack_buffer = 0
            snipear.cooldown = 0
            game_timer = 0
            hitstop = 0

        game_state = "play_state"

    if key == keys.ESCAPE and is_paused:
        exit()

    if key == keys.M : 
        is_mute = not is_mute
        if not is_mute: sounds.interact.play()

    if key == keys.ESCAPE and game_state == "play_state":
        if not is_mute: sounds.interact.play()
        enemies = []
        player.anchor = ('center', 'center')
        player.pos = (WIDTH // 2, HEIGHT // 2)
        player.anchor = ('center','bottom')
        player.health = 3
        player.iframes = 0
        player.hitstop = 0
        snipear.current_gap = snipear.base_gap
        player.sprite_animation = player.idle_animation
        player.image = player.sprite_animation[0]
        snipear.pos = (-100,-100)
        player.animation_cycle = 0
        snipear.attack_buffer = 0
        snipear.cooldown = 0
        game_timer = 0
        hitstop = 0
        game_state = "menu_state"
        is_paused = True

pgzrun.go()