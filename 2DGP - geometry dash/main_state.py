import random
import json
import os
import title_state
import maptool_state

from pico2d import *

import game_framework
import title_state
import character_class
import background_class
import tile_class
import obstacle_class



name = "MainState"


font = None
character = None
background = None
tiles = None
obstacles_triangle = None
isJump = False
speed = 0
degree = 0
real_x = 0

def enter():
    global character, background,  tiles, obstacles_triangle
    character = character_class.CHARACTER()
    background = background_class.BACKGROUND()
    # obstacle.x, obstacle.y
    obstacles_triangle = []
    # tile.x, tile.y, tile.size_x, tile.size_y, tile.mode
    # mode : 1. basic_tile  2. tile2
    tiles = []
    global speed, isJump, real_x
    speed = 2.8
    isJump = False
    real_x = 0
    ReadPos()
    pass


def exit():
    global character, background, tiles, obstacles_triangle
    del character
    del background
    del tiles
    del obstacles_triangle
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global isJump
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # 이부분은 이후 일시정지 되도록 바꾼다 -> 추가구현 내용
                game_framework.quit()
            if event.key == SDLK_m:
                game_framework.change_state(maptool_state)
        if event.type == SDL_MOUSEBUTTONDOWN:
            isJump = True
    pass


def update():
    global isJump, speed, real_x
    background.Move(speed)
    character.Move(tiles)
    for obstacle_triangle in obstacles_triangle:
        obstacle_triangle.Move(speed)
        if(obstacle_triangle.ColideCheck(character_x, character_y,character_size)):
            game_framework.quit()
    for tile in tiles:
        tile.Move(speed)
        if tile.CheckDie(character) == "die":
            game_framework.quit()
    speed += 0.0001
    real_x+=speed
    pass


def draw():
    clear_canvas()
    background.Draw()
    character.Draw()
    for obstacle in obstacles_triangle:
        obstacle.Draw()
    for tile in tiles:
        tile.Draw()
    update_canvas()
    delay(0.01)
    pass


def ReadPos():
    f = open('tile_pos.txt',mode = 'rt')
    #tile pos read

    while True:
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or (not line) or line == '':
            break
        tile_x = float(line)
        line = f.readline()
        line.strip('\n')
        if  line == 'end\n' or (not line) or line == '':
            break
        tile_y=float(line)
        line = f.readline()
        line.strip('\n')
        if  line == 'end\n' or not line or line == '':
            break
        tile_mode= int(line)
        if(tile_mode == 1):
            tiles.append(tile_class.TILE(tile_x,tile_y,100,100,1))
        elif (tile_mode == 2):
            tiles.append(tile_class.TILE(tile_x, tile_y, 70, 20, 2))


    f2 = open('triangle_obstacle_pos.txt', mode='rt')
    #triangle obstacle pos read
    while True:
        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        tri_obs_x= float(line)
        line = f2.readline()
        line.strip('\n')
        if  line == 'end\n' or not line or line == '':
            break
        tri_obs_y=float(line)
        obstacles_triangle.append(obstacle_class.OBSTACLE_TRIANGLE(tri_obs_x,tri_obs_y))

    f.close()
    f2.close()




