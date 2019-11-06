from pico2d import *

import game_framework
import maptool_state

import title_state
import character_class
import background_class
import tile_class
import obstacle_class

WORD_END_X = 24350

name = "MainState"

font = None
character = None
background = None
tiles = None
triangle_obstacles = None
isJump = False
game_speed = 0
degree = 0
camera_moving_degree_x = 0
stop = 0


def enter():
    global character, background, tiles, triangle_obstacles
    background = background_class.BACKGROUND()
    triangle_obstacles = []
    tiles = []
    character = character_class.CHARACTER()
    global camera_moving_degree_x, stop, game_speed
    game_speed = 2.8
    camera_moving_degree_x = 0
    ReadPos()
    character.tiles, character.triangle_obstacles = tiles, triangle_obstacles
    stop = 0

def exit():
    global character, background, tiles, triangle_obstacles
    del character
    del background
    del tiles
    del triangle_obstacles


def pause():
    pass


def resume():
    pass


def handle_events():
    global stop
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # 이부분은 이후 일시정지 되도록 바꾼다 -> 추가구현 내용
                game_framework.quit()
            if event.key == SDLK_m:
                # maptool 이후 릴리즈때 필요없다
                game_framework.change_state(maptool_state)
            if event.key == SDLK_s:
                # 개발자 툴로 이후 릴리즈에는 필요없다
                stop += 1
        if event.type == SDL_MOUSEBUTTONDOWN:
            character.ChangeIsJump()


def update():
    global game_speed, camera_moving_degree_x
    if stop & 2 == 0:
        game_speed += 0.0001
        # speed 만큼 카메라가 이동하였다.
        camera_moving_degree_x += game_speed
        InputGame_SpeedORCamera_Moveing_Degree()
        # background.update 내용
        background.Move()
        # character.update 내용
        character.update()
        # 시간이 지날수록 속도 빨라지게
        if character.is_death:
            game_framework.change_state(title_state)
        #print("character: ", character.is_death)



def draw():
    if stop & 2 == 0:
        clear_canvas()
        background.draw()
        character.draw()
        for obstacle in triangle_obstacles:
            obstacle.draw()
        for tile in tiles:
            tile.draw()
        update_canvas()
        delay(0.01)
    pass


def ReadPos():
    f = open('tile_pos.txt', mode='rt')
    # tile pos read
    while True:
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or (not line) or line == '':
            break
        tile_x = float(line)
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or (not line) or line == '':
            break
        tile_y = float(line)
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or not line or line == '':
            break
        tile_mode = int(line)
        if tile_mode == 1:
            tiles.append(tile_class.TILE(tile_x, tile_y, 100, 100, 1))
        elif tile_mode == 2:
            tiles.append(tile_class.TILE(tile_x, tile_y, 70, 20, 2))

    f2 = open('triangle_obstacle_pos.txt', mode='rt')
    # triangle obstacle pos read
    while True:
        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        tri_obs_x = float(line)
        line = f2.readline()
        line.strip('\n')
        if line == 'end\n' or not line or line == '':
            break
        tri_obs_y = float(line)
        triangle_obstacles.append(obstacle_class.OBSTACLE_TRIANGLE(tri_obs_x, tri_obs_y))

    f.close()
    f2.close()

def InputGame_SpeedORCamera_Moveing_Degree():
    background.GetGame_Speed(game_speed)
    character.GetCamera_Moving_Degree(camera_moving_degree_x)
    for tile in tiles:
        tile.GetCamera_Moving_Degree(camera_moving_degree_x)
    for triangle_obstacle in triangle_obstacles:
        triangle_obstacle.GetCamera_Moving_Degree(camera_moving_degree_x)
