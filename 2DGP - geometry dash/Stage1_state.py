from pico2d import *

import game_framework
import maptool_state
import game_world

import title_state
import fail_state
import character_class
import background_class
import tile_class
import obstacle_class

name = "State1 state"

WORD_END_X = 7440.704599999951

PIXEL_PER_METER = (1.0/10.0)
RUN_SPEED_KMPH = 0.01
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

font = None
character = None
background = None
tiles = None
triangle_obstacles = None
isJump = False
game_speed, temp_speed = 0, 0
degree = 0
camera_moving_degree_x = 0
stop = 0
down_p_count = 0
map_stop = False
finish_timer = 0.5


def enter():
    global character, background, tiles, triangle_obstacles, finish_timer
    background = background_class.BACKGROUND()
    background.stage = 1
    triangle_obstacles = []
    tiles = []
    character = character_class.CHARACTER()
    character.GOAL_POINT = 7190
    global camera_moving_degree_x, stop, game_speed, map_stop
    game_speed = 350.0
    camera_moving_degree_x = 0
    map_stop = False
    ReadPos()
    character.tiles, character.obstacles = tiles, triangle_obstacles
    stop = 0
    game_world.add_object(background, 0)
    game_world.add_object(character, 1)
    game_world.add_objects(tiles, 1)
    game_world.add_objects(triangle_obstacles, 1)
    finish_timer = 0.5


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global stop, temp_speed, down_p_count, game_speed
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
            if event.key == SDLK_p:
                down_p_count += 1
                if down_p_count % 2 == 1:
                    temp_speed = game_speed
                    game_speed = 800
                    character.handle_event(event)
                else:
                    game_speed = temp_speed
                    temp_speed = 0
                    character.handle_event(event)
        else:
            character.handle_event(event)


def update():
    global game_speed, camera_moving_degree_x, map_stop, finish_timer, stop
    if stop % 2 == 0:
        game_speed += RUN_SPEED_PPS
        # speed 만큼 카메라가 이동하였다.
        camera_moving_degree_x += game_speed * game_framework.frame_time
        if camera_moving_degree_x >= WORD_END_X-980:
            map_stop = True
        InputGame_SpeedORCamera_Moveing_Degree()
        # 시간이 지날수록 속도 빨라지게
        for game_object in game_world.all_objects():
            game_object.update()
    if character.is_death:
        fail_state.cur_stage = 1
        background.bgm.stop()
        finish_timer -= game_framework.frame_time
        stop = 1
        if finish_timer < 0:
            game_framework.change_state(fail_state)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
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
        elif tile_mode == 3:
            tiles.append(tile_class.TILE(tile_x, tile_y, 70, 20, 3))

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
    character.GetCamera_Moving_Degree(camera_moving_degree_x)
    background.GetGame_Speed(game_speed * game_framework.frame_time)
    if not map_stop:
        for tile in tiles:
            tile.GetCamera_Moving_Degree(camera_moving_degree_x)
        for triangle_obstacle in triangle_obstacles:
            triangle_obstacle.GetCamera_Moving_Degree(camera_moving_degree_x)
    if map_stop:
        background.GetGame_Speed(0)
        character.map_stop = True
