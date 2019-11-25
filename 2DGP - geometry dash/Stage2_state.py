from pico2d import *

import game_framework
import maptool2_state
import game_world

import fail_state
import character_class
import background_class
import tile_class
import rectangle_obstacle_class
import ufo_class

name = "Stage2 State"

# 맵이 완성된 후 값을 바꿔준다
WORD_END_X = 10000.704599999951
VIHICLE_START_POINT = 1000

PIXEL_PER_METER = (3.0 / 1.0)
RUN_SPEED_KMPH = 0.2
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

font = None
character, background, tiles, rectangle_obstacles, ufo = None, None, None, None, None
isJump = False
game_speed, temp_speed = 0, 0
degree = 0
camera_moving_degree_x = 0
stop = 0
down_p_count = 0
map_stop = False


def enter():
    global character, background, tiles, rectangle_obstacles, ufo
    background = background_class.BACKGROUND()
    background.image_1 = load_image('background2.png')
    background.image_2 = load_image('background2.png')
    background.image_3 = load_image('background2.png')
    background.stage = 2
    tiles, rectangle_obstacles = [], []
    character = character_class.CHARACTER()
    character.GOAL_POINT = 9903.68660381633
    ufo = ufo_class.UFO()
    global camera_moving_degree_x, stop, game_speed, map_stop
    game_speed = 600.0
    camera_moving_degree_x = 0
    map_stop = False
    ReadPos()
    character.tiles = tiles
    character.obstacles = rectangle_obstacles
    character.ufo = ufo
    ufo.tiles = tiles
    ufo.obstacles = rectangle_obstacles
    stop = 0
    game_world.add_object(background, 0)
    game_world.add_object(character, 1)
    game_world.add_object(ufo, 1)
    game_world.add_objects(tiles, 1)
    game_world.add_objects(rectangle_obstacles, 1)


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
                game_framework.change_state(maptool2_state)
            if event.key == SDLK_s:
                # 개발자 툴로 이후 릴리즈에는 필요없다
                stop += 1
            if event.key == SDLK_p:
                down_p_count += 1
                if down_p_count % 2 == 1:
                    temp_speed = game_speed
                    # game_speed = 800
                    character.handle_event(event)
                    ufo.handle_event(event)
                else:
                    game_speed = temp_speed
                    temp_speed = 0
                    character.handle_event(event)
                    ufo.handle_event(event)
        else:
            character.handle_event(event)
            ufo.handle_event(event)


def update():
    global game_speed, camera_moving_degree_x, map_stop
    if stop & 2 == 0:
        game_speed += RUN_SPEED_PPS
        # speed 만큼 카메라가 이동하였다.
        camera_moving_degree_x += game_speed * game_framework.frame_time
        if camera_moving_degree_x >= WORD_END_X - 980:
            map_stop = True
        if VIHICLE_START_POINT <= character.x < character_class.GET_OFF_POS:
            character.ride_ufo = True
            ufo.move = True
        InputGame_SpeedORCamera_Moveing_Degree()
        # 시간이 지날수록 속도 빨라지게
        for game_object in game_world.all_objects():
            game_object.update()
        if character.is_death or ufo.collide:
            fail_state.cur_stage = 2
            game_framework.change_state(fail_state)


def draw():
    if stop & 2 == 0:
        clear_canvas()
        for game_object in game_world.all_objects():
            game_object.draw()
        update_canvas()
        delay(0.01)
    pass


def ReadPos():
    f = open('stage2_tile_pos.txt', mode='rt')
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
        tiles.append(tile_class.TILE(tile_x, tile_y, 100, 100, 1))

    f2 = open('rect_obs_pos.txt', mode='rt')
    # rectangle obstacle pos read
    while True:
        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        rect_obs_x = float(line)

        line = f2.readline()
        line.strip('\n')
        if line == 'end\n' or not line or line == '':
            break
        rect_obs_y = float(line)

        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        rect_obs_size = float(line)

        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        mode = int(line)
        rectangle_obstacles.append(
            rectangle_obstacle_class.RECTANGLE_OBSTCLE(rect_obs_x, rect_obs_y, rect_obs_size, mode))

    f.close()
    f2.close()


def InputGame_SpeedORCamera_Moveing_Degree():
    character.GetCamera_Moving_Degree(camera_moving_degree_x)
    background.GetGame_Speed(game_speed * game_framework.frame_time)
    ufo.GetCamera_Moving_Degree(camera_moving_degree_x)
    if not map_stop:
        for tile in tiles:
            tile.GetCamera_Moving_Degree(camera_moving_degree_x)
        for rectangle_obstacle in rectangle_obstacles:
            rectangle_obstacle.GetCamera_Moving_Degree(camera_moving_degree_x)
    if map_stop:
        background.GetGame_Speed(0)
        character.map_stop = True
