''' DISCLAMER: Its not possible to center the game window on Windows with pure Pgzero alone and
for the limitations there were given to this project, i cannot "import os". It's a small issue
that will only be a problem in the moment that you open the game, but i think is good to put
the option if you so much disere '''

### CENTER THE WINDOW ON LAUNCH, if it's not doing already (DE-COMMENT TO ACTIVATE) ###
#import os
#os.environ['SDL_VIDEO_CENTERED'] = '1'

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
key_cooldown = 0

background = Actor('background')

game_timer = 0
game_score = 0
game_state = "menu_state"

is_paused = True
hitstop = 0 # hit "pause" effect

player = Player()
snipear = Snipear(player)

mouse_pos = (0, 0)

enemies = []
spawn_timer = random.choice((20,40,60))

def spawn_manager():

    global spawn_timer, game_timer

    spawn_timer -= 1

    if spawn_timer <= 0 and len(enemies) < 25:

        spawn_timer = random.choice((0,30,60,90,120)) - min(game_timer // 150, 60)
        spawn_pos = ()

        spawn_axi = random.choice(("x","y"))
        
        if spawn_axi == "x":   spawn_pos = (random.choice((-80,WIDTH + 80)), random.randint(-80, HEIGHT + 80))
        elif spawn_axi == "y": spawn_pos = (random.randint(-80,WIDTH + 80), random.choice((-80, HEIGHT + 80)))

        enemies.append(Enemy(spawn_pos))

def enemy_self_collision(enemy):

    for other in enemies:

        if enemy != other:
        
            dist = max(math.sqrt((enemy.x - other.x)**2 + (enemy.y - other.y)**2), 1)
            
            if dist < 40:

                enemy.x -= (other.x - enemy.x) / dist * 0.5
                enemy.y -= (other.y - enemy.y) / dist * 0.5

def collision_to_player(enemy):

    global hitstop, music_vol

    if enemy.hitbox().colliderect(player.hitbox()) and player.iframes == 0: 

        if not is_mute: sounds.player_hurt.play()

        snipear.impacts.append({"pos":player.topleft, "life":1})

        player.health -= 1
        player.iframes = 120
        
        music_vol = 0
        hitstop = 8

def enemy_manager():

    spawn_manager()

    for enemy in enemies:

        enemy.follow(player.pos)
        enemy_self_collision(enemy)
        collision_to_player(enemy)

def on_mouse_move(pos):

    global mouse_pos
    mouse_pos = pos

def on_mouse_down(button, pos):

    global is_paused, game_state, is_mute

    if button == mouse.RIGHT and not is_paused: snipear.shot_buffer = 10 # Shot input
    elif button == mouse.LEFT and not is_paused: snipear.attack_buffer = 10 # Attack input

    if button == mouse.LEFT and is_paused:

        # START/RESTART
        if btn_start_rect.collidepoint(pos):
            if not is_mute: sounds.interact.play()
            if game_state == "restart_state": reset_attributes()
            game_state = "play_state"
            is_paused = False
            music.play('bgm')

        # MUTE
        elif btn_mute_rect.collidepoint(pos):
            is_mute = not is_mute
            sounds.interact.play()

        # QUIT
        elif btn_quit_rect.collidepoint(pos):

            if game_state == "restart_state": 

                reset_attributes()
                game_state = "menu_state"

            else: exit() 

def update():

    global game_timer, game_state, is_paused, hitstop, music_vol, is_mute, key_cooldown

    ### Always running ###

    key_cooldown = max(key_cooldown - 1, 0)

    if is_mute or is_paused: music_vol = 0

    if game_state == "play_state":

        if hitstop != 0: is_paused = True
        else: is_paused = False

    hitstop = max(hitstop - 1, 0)

    music.set_volume(music_vol)
    if not is_mute: music_vol += (.75 - music_vol) * .01

    if is_paused: return

    ### Play state loop ###

    game_timer += 1

    player.move(keyboard)

    player.iframes = max(player.iframes - 1, 0)
    
    if player.iframes % 3 == 0: player.hitflash = not player.hitflash
    if player.iframes == 0: player.hitflash = False

    enemy_manager()

    if player.health == 0: # Game Over

        game_state = "restart_state"
        is_paused = True
        return

    snipear.update(mouse_pos, enemies, is_mute)

def animate(obj): 

    if obj.animation_cycle == -1: return 
    obj.animation_cycle += .1
    obj.animation_cycle = obj.animation_cycle % len(obj.sprite_animation)
    obj.image = obj.sprite_animation[math.floor(obj.animation_cycle)]

btn_start_rect = Rect(0, 0, 250, 40)
btn_start_rect.center = (WIDTH // 2, HEIGHT // 2 + 80)

btn_mute_rect = Rect(0, 0, 250, 40)
btn_mute_rect.center = (WIDTH // 2, HEIGHT // 2 + 120)

btn_quit_rect = Rect(0, 0, 250, 40)
btn_quit_rect.center = (WIDTH // 2, HEIGHT // 2 + 160)

def draw():

    global game_state, game_score, game_timer, hitstop

    background.draw()

    if game_state == "menu_state":
        screen.fill((34,32,52))
        screen.draw.text(
            "HEPHAESTUZ",
            center=(WIDTH // 2, HEIGHT // 2 - 80), 
            fontsize=120, 
            fontname=FONT,
            color="white",
            shadow=(1, 1),
            scolor=(34,32,52)
        )

        screen.draw.text(
            f"ENTER Start || M to {"Mute" if not is_mute else "Demute"} || ESC to Quit", 
            center=(WIDTH // 2, HEIGHT - 10), 
            fontsize=20, 
            fontname=FONT,
            color="grey",
            shadow=(2, 2),
            scolor=(34,32,52)
        )

    render_list = [player, snipear] + enemies
    render_list.sort(key=lambda obj: obj.y)

    for obj in render_list:

        if obj.has_shadow and not is_paused:
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

            screen.blit('impact', impact["pos"])
            if hitstop == 0: 

                impact["life"] -= 1
                if impact["life"] == 0: snipear.impacts.remove(impact)

    if snipear.shot_trail["life"] > 0:
        
        if snipear.shot_cooldown == snipear.shot_attack_speed: 
            snipear.shot_cooldown  -= 1 
            hitstop = 5

        angle_rad = math.atan2(
            snipear.shot_trail["end_pos"][1] - snipear.shot_trail["init_pos"][1],
            snipear.shot_trail["end_pos"][0] - snipear.shot_trail["init_pos"][0]
        )
        perp_angle = angle_rad + math.pi / 2 

        for width in range(-4, 5):
     
            offset_x = math.cos(perp_angle) * width / 2
            offset_y = math.sin(perp_angle) * width / 2
            
            screen.draw.line(
                (snipear.shot_trail["init_pos"][0] + offset_x, snipear.shot_trail["init_pos"][1] + offset_y),
                (snipear.shot_trail["end_pos"][0] + offset_x, snipear.shot_trail["end_pos"][1] + offset_y),
                color='white'
            )
        
        if hitstop == 0:
            snipear.shot_trail["life"] -= 1

    if game_state == "play_state":

        screen.draw.text(
            f"AWSD to Move || LEFT-CLICK to Attack || RIGHT-CLICK to Shot || M to {"Mute" if not is_mute else "Demute"} || ESC to return to Menu ", 
            center=(WIDTH // 2, HEIGHT - 10), 
            fontsize=20, 
            fontname=FONT,
            color="grey",
            shadow=(2, 2),
            scolor=(34,32,52)
        )

        for i in range(-1,2):
            pos = (WIDTH // 2 + 64 * i - 24, 8)
            if player.health >= i + 2:
                screen.blit('health', pos)
            else:
                screen.blit('health_slot', pos)

        mins = str(game_timer // 3600)
        for i in range(2 - len(mins)) : mins = "0" + mins
        secs = str((game_timer // 60) % 60)
        for i in range(2 - len(secs)) : secs = "0" + secs

        screen.draw.text(
            f"TIME: {mins}:{secs}", 
            topleft=(8, 8), 
            fontsize=40, 
            fontname=FONT,
            color="white",
            shadow=(1, 1),
            scolor=(34,32,52)
        )

        game_score = snipear.kills
        text = str(int(game_score * 10))
        for i in range(6 - len(text)): text = "0" + text

        screen.draw.text(
            f"SCORE: {text}", 
            topright=(WIDTH - 8, 8), 
            fontsize=40, 
            fontname=FONT,
            color="white",
            shadow=(1, 1),
            scolor=(34,32,52)
        )
    
    if game_state == "restart_state":

        screen.fill((34,32,52))

        screen.draw.text(
            "GAMEOVER", 
            center=(WIDTH // 2, HEIGHT // 2 - 80), 
            fontsize=120, 
            fontname=FONT,
            color="white",
            shadow=(1, 1),
            scolor=(34,32,52)
        )

        screen.blit('player_idle_1', (WIDTH // 2 - player.width // 2, HEIGHT // 2 - player.height // 2))

        screen.draw.text(
            f"ENTER Restart || M to {"Mute" if not is_mute else "Demute"} || ESC to go to Menu", 
            center=(WIDTH // 2, HEIGHT - 10), 
            fontsize=20, 
            fontname=FONT,
            color="grey",
            shadow=(2, 2),
            scolor=(34,32,52)
        )

    # Menu Buttons

    if is_paused and not game_state == "play_state":

        screen.draw.text(
            "START" if game_state == "menu_state" else "RESTART", 
            center=(WIDTH // 2, HEIGHT // 2 + 80), 
            fontsize=30, 
            fontname=FONT,
            color="white" if btn_start_rect.collidepoint(mouse_pos) else "grey",
            shadow=(1, 1),
            scolor=(34,32,52)
        )
        screen.draw.text(
            "MUTE" if not is_mute else "DEMUTE", 
            center=(WIDTH // 2, HEIGHT // 2 + 120), 
            fontsize=30, 
            fontname=FONT,
            color="white" if btn_mute_rect.collidepoint(mouse_pos) else "grey",
            shadow=(1, 1),
            scolor=(34,32,52)
        )
        screen.draw.text(
            "QUIT" if game_state == "menu_state" else "RETURN TO MENU", 
            center=(WIDTH // 2, HEIGHT // 2 + 160), 
            fontsize=30, 
            fontname=FONT,
            color="white" if btn_quit_rect.collidepoint(mouse_pos) else "grey",
            shadow=(1, 1),
            scolor=(34,32,52)
        )

def reset_attributes():

    global spawn_timer, game_timer, game_state, hitstop, enemies, game_score

    # Game attributes
    game_score = 0
    game_timer = 0

    enemies = []
    spawn_timer = random.choice((20,40,60))

    hitstop = 0

    # Player
    player.anchor = ('center', 'center')
    player.pos = (WIDTH // 2, HEIGHT // 2)
    player.anchor = ('center','bottom')

    player.health = 3
    player.iframes = 0

    player.sprite_animation = player.idle_animation
    player.image = player.sprite_animation[0]
    player.animation_cycle = 0
    player.hitflash = False

    # Snipear
    snipear.kills = 0

    snipear.attack_buffer = 0
    snipear.cooldown = 0
    snipear.shot_buffer = 0
    snipear.shot_cooldown = 0

    snipear.current_gap = snipear.base_gap
    snipear.pos = (-100,-100)
      
def on_key_down(key):

    global spawn_timer, game_timer, game_state, is_paused, hitstop, enemies, is_mute, game_score, key_cooldown

    if key_cooldown == 0:

         # Start (or Restart) the game
        if key == keys.RETURN and (game_state == "restart_state" or game_state == "menu_state"):

            key_cooldown = 30
            if not is_mute: sounds.interact.play()

            music.play('bgm')
            music_vol = 0
            is_paused = False

            if game_state == "restart_state": reset_attributes()
            game_state = "play_state"

        # Mute (or Demute)
        elif key == keys.M : 

            key_cooldown = 30
            sounds.interact.play()

            is_mute = not is_mute

        # Go back to menu
        elif key == keys.ESCAPE and game_state == "play_state":

            key_cooldown = 30
            if not is_mute: sounds.interact.play()

            reset_attributes()
            game_state = "menu_state"
            is_paused = True

        # Quit
        elif key == keys.ESCAPE and is_paused: exit()

pgzrun.go()