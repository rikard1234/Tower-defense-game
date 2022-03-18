#import libraries
import os
import pygame
import math
import random

from pygame import transform

import button
from Enemy import Enemy
from Castle import Castle
from Bullet import Bullet
from Tower import Tower
from Crosshair import Crosshair
from Friend import Friend
from Snowball import Snowball
from Boss import Boss
music_file = 'mp3/1.wav'
##############################################################################################################################
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1)
##############################################################################################################################
#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Castle Defender')
clock = pygame.time.Clock()
FPS = 60
##############################################################################################################################
#define game viariables
game_state = [
    'menu',
    'game'
]
boss_spawned = False
enemy_selector = 1
state_selector = 0
high_score = 0
level = 1
level_difficulty = 0
target_difficulty = 300
DIFFICULTY_MULTIPLIER = 1.75
game_over = False
next_level = False
ENEMY_TIMER = 1000
TOWER_COST = 5000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
max_towers = 4
tower_positions = [
    [SCREEN_WIDTH - 250, SCREEN_HEIGHT - 200],
    [SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150],
]
snowbal_position = [
    [SCREEN_WIDTH - 800, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 750, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 700, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 650, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 600, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 550, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 500, SCREEN_HEIGHT - 550],
    [SCREEN_WIDTH - 450, SCREEN_HEIGHT - 550],
]
##############################################################################################################################
#define font
font = pygame.font.SysFont('Futura', 30)
font_60 = pygame.font.SysFont('Futura', 60)
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
##############################################################################################################################
#define colours
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLUE = (0, 0, 102)
##############################################################################################################################

#load images

bg = pygame.image.load('img/bg.png').convert_alpha()
menu = pygame.image.load('img/menu.png').convert_alpha()

#bullet
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

#castle
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
castle_img_50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_img_25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()

#tower
tower_img_100 = pygame.image.load('img/tower/tower_100.png').convert_alpha()
tower_img_50 = pygame.image.load('img/tower/tower_50.png').convert_alpha()
tower_img_25 = pygame.image.load('img/tower/tower_25.png').convert_alpha()

#magic

snowball_img = pygame.image.load('img/snowball.png').convert_alpha()
s_w = snowball_img.get_width()
s_h = snowball_img.get_height()
snowball_img = pygame.transform.scale(snowball_img, (int(s_w * 0.2), int(s_h * 0.1)))

#button images
repair_button = pygame.image.load('img/repair.png').convert_alpha()
armour_button = pygame.image.load('img/armour.png').convert_alpha()
startButton = pygame.image.load('img/startButtonT.png').convert_alpha()
startButton1 = pygame.image.load('img/startButton1.png').convert_alpha()
pomocnik_button = pygame.image.load('img/pomocnik.png').convert_alpha()
magicsnow_button = pygame.image.load('img/magicsnow.png').convert_alpha()
wind_magic_button = pygame.image.load('img/magicwind.png.').convert_alpha()
magicsnow_button1 = pygame.image.load('img/magicsnow1.png').convert_alpha()
wind_magic_button1 = pygame.image.load('img/magicwind1.png').convert_alpha()
##############################################################################################################################
enemy_animations = []
boss_animations = []
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin', 'pomocnik']
boss_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin', 'pomocnik']
enemy_health = [75, 100, 125, 150]
boss_health = [300, 400, 500, 600]

animation_types = ['walk', 'attack', 'death']
###################################################################################################################3
for enemy in enemy_types:
    #load animation
    animation_list = []
    for animation in animation_types:
        #reset temporary list of images
        temp_list = []
        #define number of frames
        num_of_frames = 20
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)
##############################################################################################################################
for boss in boss_types:
    #load animation
    animation_list_boss = []
    for animation in animation_types:
        #reset temporary list of images
        temp_list_boss = []
        #define number of frames
        num_of_frames = 20
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/enemies/{boss}/{animation}/{i}.png').convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.8), int(e_h * 0.8)))
            temp_list_boss.append(img)
        animation_list_boss.append(temp_list_boss)
    boss_animations.append(animation_list_boss)
#function for outputtin gtext on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def show_info():
    draw_text('Money ' + str(castle.money), font, GREY, 10, 10)
    draw_text('Score ' + str(castle.score), font, GREY, 180, 10)
    draw_text('High score ' + str(high_score), font, GREY, 180, 30)
    draw_text('Level ' + str(level), font, GREY, SCREEN_WIDTH // 2, 10)
    draw_text('Health ' + str(castle.health) + '/' + str(castle.max_health), font, GREY, SCREEN_WIDTH - 230, SCREEN_HEIGHT - 50)
    draw_text(str(TOWER_COST), font, GREY, SCREEN_WIDTH - 150, 70)
    draw_text('1000 ', font, GREY, SCREEN_WIDTH - 225, 70)
    draw_text('1000 ', font, GREY, SCREEN_WIDTH - 300, 70)
    draw_text('1000 ', font, GREY, SCREEN_WIDTH - 75, 70)
    draw_text('1000 ', font, BLUE, SCREEN_WIDTH - 110, 180)
    draw_text('5000 ', font, BLUE, SCREEN_WIDTH - 110, 280)

repair = button.Button(SCREEN_WIDTH - 220, 10, repair_button, 0.5)
armour = button.Button(SCREEN_WIDTH - 70, 10, armour_button, 1.5)
tower_button = button.Button(SCREEN_WIDTH - 140, 10, tower_img_100, 0.1)
startButton = button.Button(SCREEN_WIDTH - 600, 200, startButton, 0.5, startButton1)
pomocnikButton =  button.Button(SCREEN_WIDTH - 350, -25, pomocnik_button, 0.2)
wind_magic = button.Button(SCREEN_WIDTH - 120, 110, wind_magic_button, 0.1, wind_magic_button1)
magic_snow = button.Button(SCREEN_WIDTH - 120, 220, magicsnow_button, 0.1, magicsnow_button1)
##############################################################################################################################
#creation section
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

crosshair = Crosshair(0.025)


#create groups
tower_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
friend_group = pygame.sprite.Group()
snowball_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
enemy_group_list = []
#create enemies


##############################################################################################################################
#game loop
run = True
while run:
    clock.tick(FPS)
    if(game_state[state_selector] == 'menu'):
        pygame.mouse.set_visible(True)
        screen.blit(menu, (0, 0))
        if startButton.draw(screen):
            state_selector = 1

    if(game_state[state_selector] == 'game'):
        pygame.mouse.set_visible(False)
        if game_over == False:
            screen.blit(bg, (0, 0))
            #draw castle
            castle.draw()
            castle.shoot(bullet_img, bullet_group)
            #draw tower
            tower_group.draw(screen)
            tower_group.update(enemy_group, bullet_img, bullet_group, castle, boss_group)
            #draw crosshair
            crosshair.draw()
            #draw bullets
            bullet_group.update()
            bullet_group.draw(screen)

            #draw snowball
            snowball_group.update(enemy_group)
            snowball_group.draw(screen)

            #draw enemies
            enemy_group.update(screen, castle, bullet_group, friend_group, snowball_group)
            friend_group.update(screen, castle, enemy_group, boss_group)
            boss_group.update(screen, castle, bullet_group, friend_group, snowball_group)

            show_info()
            if magic_snow.draw(screen) and castle.money >= 5000:
                castle.money -= 5000
                #for position in snowbal_position:
                for index in range (len(snowbal_position)):
                    snowball = Snowball(snowball_img, snowbal_position[index][0], snowbal_position[index][1], 2)
                    snowball_group.add(snowball)

            if pomocnikButton.draw(screen):
                    if castle.money >= 1000:
                        friend = Friend(50, enemy_animations[4], 500, SCREEN_HEIGHT - 135, 1)
                        friend_group.add(friend)
                        castle.money -= 1000

            if wind_magic.draw(screen) and castle.money >= 1000:
                castle.money -= 1000
                for e in enemy_group_list:
                    e.react_to_wind()

            if repair.draw(screen):
                castle.repair()
            if armour.draw(screen):
                castle.armour()
            if tower_button.draw(screen):
                #check if there is enough money
                if castle.money >= TOWER_COST and len(tower_group) < max_towers:
                    tower = Tower(tower_img_100,
                                  tower_img_50,
                                  tower_img_25,
                                  tower_positions[len(tower_group)][0],
                                  tower_positions[len(tower_group)][1],
                                  0.2
                                  )
                    tower_group.add(tower)
                    castle.money -= TOWER_COST

            #create enemies
            #check if max number of enemies has been reached
            if level_difficulty < target_difficulty:
                if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER and level % 5 != 0:
                    e = random.randint(0, enemy_selector)
                    enemy = Enemy(enemy_health[e] * DIFFICULTY_MULTIPLIER, enemy_animations[e], -100, SCREEN_HEIGHT - 100, (1 + level // 5))
                    enemy_group.add(enemy)
                    enemy_group_list.append(enemy)
                    last_enemy = pygame.time.get_ticks()
                    level_difficulty += enemy_health[e]
                if level % 5 == 0 and boss_spawned == False:
                    boss_spawned = True
                    e = random.randint(0, 2)
                    boss = Boss(boss_health[e] * DIFFICULTY_MULTIPLIER, boss_animations[e], -100, SCREEN_HEIGHT - 80, 1 * DIFFICULTY_MULTIPLIER)
                    boss_group.add(boss)
                    level_difficulty += 10000

            #chceck if all the enemies have been spawned
            if level_difficulty >= target_difficulty:
                #check how many are still alive
                enemies_alive = 0
                boss_alive = 0
                for e in enemy_group:
                    if e.alive == True:
                        enemies_alive += 1

                for e in boss_group:
                    if e.alive == True:
                        boss_alive += 1

                if boss_alive == 0 and next_level == False and level % 5 == 0:
                    next_level = True
                    level_reset_time = pygame.time.get_ticks()

                if enemies_alive == 0 and next_level == False and level % 5 != 0:
                    next_level = True
                    level_reset_time = pygame.time.get_ticks()

            #move onto the next level
            if next_level == True:
                draw_text('LEVEL COMPLETE', font_60, WHITE, 200, 300)
                #update highscore
                if castle.score > high_score:
                    high_score = castle.score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                if pygame.time.get_ticks() - level_reset_time > 1500:
                    next_level = False
                    level += 1
                    last_enemy = pygame.time.get_ticks()
                    target_difficulty *= DIFFICULTY_MULTIPLIER
                    level_difficulty = 0
                    enemy_selector = (enemy_selector + 1) % 4
                    boss_group.empty()
                    enemy_group.empty()
                    boss_spawned = False
            if castle.health <= 0:
                game_over = True
        else:
            draw_text('GAME OVER', font, GREY, 300, 300)
            draw_text('PRESS A TO PLAY AGAIN', font, GREY, 250, 250)
            pygame.mouse.set_visible(True)
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                game_over = False
                next_level = False
                level = 1
                target_difficulty = 1000
                level_difficulty = 0
                last_enemy = pygame.time.get_ticks()
                enemy_group.empty()
                tower_group.empty()
                enemy_group_list.clear()
                castle.score = 0
                castle.health = 1000
                castle.max_health = castle.health
                castle.money = 5000
                pygame.mouse.set_visible(False)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display window
    pygame.display.update()

pygame.quit()