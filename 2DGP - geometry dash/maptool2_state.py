import game_framework
import Stage1_state
from pico2d import *

name = "MaptoolState"

PIXEL_PER_METER = (3.0 / 1.0)
RUN_SPEED_KMPH = 0.01
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

import background_class
import tile_class
import rectangle_obstacle_class
import Stage2_state

background = None
home = None
mode, kind = 0, 0
tile_x, tile_y, rect_obs_x, rect_obs_y, rect_obs_size, rect_obs_mode = [], [], [], [], [],[]
x, y, mx, my, size_x, size_y = 0, 0, 0, 0, 0, 0
image = None
speed, inspeed, temp_speed = 0.28, 0, 0
stop = True
tiles, rect_obses = [], []
camera_x = 0
delete_idx = 0
down_p_count = 0


def enter():
    global mode, kind
    mode = 't'
    kind = 1
    global tile_x, tile_y, rect_obs_x, rect_obs_y, rect_obs_size
    tile_x, tile_y, rect_obs_x, rect_obs_y, rect_obs_size,rect_obs_mode = [], [], [], [], [], []
    global image
    image = load_image('basic_tile.png')

    global x, y, mx, my, size_x, size_y, camera_x, stop
    size_x = 100
    size_y = 100
    camera_moving_degree_x = 0
    stop = True

    global background, speed, inspeed
    background = background_class.BACKGROUND()
    background.image_1 = load_image('background2.png')
    background.image_2 = load_image('background2.png')
    background.image_3 = load_image('background2.png')
    speed = 270
    inspeed = 0

    global tiles, rect_obses, delete_idx
    delete_idx = "tile"

    ReadPos()
    pass


def exit():
    # 모드를 나갈때 txt파일에 각 장애물, 타일의 pos값을 저장한다.
    f = open('stage2_tile_pos.txt', mode='wt')
    for i in range(len(tiles)):
        f.write(str(tile_x[i]))
        f.write('\n')
        f.write(str(tile_y[i]))
        f.write('\n')
    f.write('end\n')

    f2 = open('rect_obs_pos.txt', mode='wt')
    for i in range(len(rect_obses)):
        f2.write(str(rect_obs_x[i]))
        f2.write('\n')
        f2.write(str(rect_obs_y[i]))
        f2.write('\n')
        f2.write(str(rect_obs_size[i]))
        f2.write('\n')
        f2.write(str(rect_obs_mode[i]))
        f2.write('\n')
    f2.write('end\n')
    f.close()
    f2.close()

    global background, image
    del background
    del image


def pause():
    pass


def resume():
    pass


def handle_events():
    global image, size_x, size_y, mx, my, x, y, inspeed, stop, mode, kind, down_p_count, temp_speed, speed, obs_mode
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if (event.key == SDLK_t):
                # tile selection
                mode = 't'
                if (kind == 1):
                    image = load_image('basic_tile.png')
                    size_x = 100
                    size_y = 100
            if event.key == SDLK_o:
                # obstacle selection
                mode = 'o'
                if (kind == 1):
                    image = load_image('Rect_Obstacle100x100.png')
                    size_x = 100
                    size_y = 100
                    obs_mode = 1
                elif (kind == 2):
                    image = load_image('Rect_Obstacle150x150.png')
                    size_x = 150
                    size_y = 150
                    obs_mode = 1
                elif kind == 3:
                    image = load_image('Rect_Obstacle200x200.png')
                    size_x = 200
                    size_y = 200
                    obs_mode = 1
                elif kind == 4:
                    image = load_image('Rect_Obstacle250x250.png')
                    size_x = 250
                    size_y = 250
                    obs_mode = 1
                elif kind == 5:
                    image = load_image('Rect_Obstacle300x300.png')
                    size_x = 300
                    size_y = 300
                    obs_mode = 1
                elif kind == 6:
                    image = load_image('Reverse_Gate.png')
                    size_x = 150
                    size_y = 160
                    obs_mode = 2
            if (event.key == SDLK_1):
                kind = 1
                if (mode == 't'):
                    image = load_image('basic_tile.png')
                    size_x = 100
                    size_y = 100
                elif (mode == 'o'):
                    image = load_image('Rect_Obstacle100x100.png')
                    size_x = 100
                    size_y = 100
                    obs_mode = 1
            if event.key == SDLK_2:
                kind = 2
                if (mode == 'o'):
                    image = load_image('Rect_Obstacle150x150.png')
                    size_x = 150
                    size_y = 150
                    obs_mode = 1
            if event.key == SDLK_3:
                kind = 3
                if (mode == 'o'):
                    image = load_image('Rect_Obstacle200x200.png')
                    size_x = 200
                    size_y = 200
                    obs_mode = 1
            if event.key == SDLK_4:
                kind = 4
                if (mode == 'o'):
                    image = load_image('Rect_Obstacle250x250.png')
                    size_x = 250
                    size_y = 250
                    obs_mode = 1
            if event.key == SDLK_5:
                kind = 5
                if (mode == 'o'):
                    image = load_image('Rect_Obstacle300x300.png')
                    size_x = 300
                    size_y = 300
                    obs_mode = 1
            if event.key == SDLK_6:
                kind = 6
                if (mode == 'o'):
                    image = load_image('Reverse_Gate.png')
                    size_x = 150
                    size_y = 150
                    obs_mode = 2
            if event.key == SDLK_BACKSPACE:
                DeleteBlock()
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_s:
                inspeed = 0
                stop = True
            if event.key == SDLK_r:
                inspeed = speed
                stop = False
            if event.key == SDLK_m:
                game_framework.change_state(Stage2_state)
            if event.key == SDLK_p:
                down_p_count += 1
                if down_p_count % 2 == 1:
                    temp_speed = speed
                    speed = 800
                else:
                    speed = temp_speed
                    temp_speed = 0
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x = event.x
            y = 510 - event.y - 1
            Create()
        elif event.type == SDL_MOUSEMOTION:
            mx = event.x
            my = 510 - event.y - 1

    pass


def update():
    global speed, camera_x, inspeed, speed
    if (stop == False):
        InputGame_SpeedORCamera_Moveing_Degree()
        #InputGame_Speed()
        background.Move()
        speed += RUN_SPEED_PPS
        inspeed = speed
        camera_x += inspeed*game_framework.frame_time
    delay(0.01)
    pass


def draw():
    hide_cursor()
    clear_canvas()
    background.draw()
    image.draw(mx, my, size_x, size_y)
    for tile in tiles:
        tile.draw()
    for rect_obs in rect_obses:
        rect_obs.draw()
    update_canvas()

    pass


def Create():
    global delete_idx
    if mode == 't' and kind == 1:
        # basic tile
        tiles.append(tile_class.TILE(x, y, size_x, size_y, 1))
        tile_x.append(x + camera_x - 10)
        tile_y.append(y)
        delete_idx = "tile"
    elif mode == 'o' and kind == 1:
        # triangle obstacle
        rect_obses.append(rectangle_obstacle_class.RECTANGLE_OBSTCLE(x, y, size_x,1))
        rect_obs_x.append(x + camera_x - 10)
        rect_obs_y.append(y)
        rect_obs_size.append(size_x)
        rect_obs_mode.append(obs_mode)
        delete_idx = "rect_obs"
    elif mode == 'o' and kind == 2:
        # triangle obstacle
        rect_obses.append(rectangle_obstacle_class.RECTANGLE_OBSTCLE(x, y, size_x,1))
        rect_obs_x.append(x + camera_x - 10)
        rect_obs_y.append(y)
        rect_obs_size.append(size_x)
        rect_obs_mode.append(obs_mode)
        delete_idx = "rect_obs"
    elif mode == 'o' and kind == 3:
        # triangle obstacle
        rect_obses.append(rectangle_obstacle_class.RECTANGLE_OBSTCLE(x, y, size_x,1))
        rect_obs_x.append(x + camera_x - 10)
        rect_obs_y.append(y)
        rect_obs_size.append(size_x)
        rect_obs_mode.append(obs_mode)
        delete_idx = "rect_obs"
    elif mode == 'o' and kind == 4:
        # triangle obstacle
        rect_obses.append(rectangle_obstacle_class.RECTANGLE_OBSTCLE(x, y, size_x,1))
        rect_obs_x.append(x + camera_x - 10)
        rect_obs_y.append(y)
        rect_obs_size.append(size_x)
        rect_obs_mode.append(obs_mode)
        delete_idx = "rect_obs"
    elif mode == 'o' and kind == 5:
        # triangle obstacle
        rect_obses.append(rectangle_obstacle_class.RECTANGLE_OBSTCLE(x, y, size_x,1))
        rect_obs_x.append(x + camera_x - 10)
        rect_obs_y.append(y)
        rect_obs_size.append(size_x)
        rect_obs_mode.append(obs_mode)
        delete_idx = "rect_obs"
    elif mode == 'o' and kind == 6:
        rect_obses.append(rectangle_obstacle_class.RECTANGLE_OBSTCLE(x, y, size_x,2))
        rect_obs_x.append(x + camera_x - 10)
        rect_obs_y.append(y)
        rect_obs_size.append(size_x)
        rect_obs_mode.append(obs_mode)
        delete_idx = "rect_obs"

    pass


def DeleteBlock():
    if (delete_idx == "tile"):
        del tiles[len(tiles) - 1]
        del tile_x[len(tiles) - 1]
        del tile_y[len(tiles) - 1]

    if delete_idx == "rect_obs":
        del rect_obses[len(rect_obses) - 1]
        del rect_obs_y[len(rect_obs_y) - 1]
        del rect_obs_x[len(rect_obs_x) - 1]
        del rect_obs_size[len(rect_obs_size) - 1]
    pass


def ReadPos():
    global tile_x, tile_y, rect_obs_mode, rect_obs_x, rect_obs_y, tiles, rect_obses
    f = open('stage2_tile_pos.txt', mode='rt')
    # tile pos read
    while True:
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or (not line) or line == '':
            break
        tile_x.append(float(line))
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or (not line) or line == '':
            break
        tile_y.append(float(line))
        tiles.append(tile_class.TILE(tile_x[len(tile_x) - 1], tile_y[len(tile_x) - 1], 100, 100, 1))

    f2 = open('rect_obs_pos.txt', mode='rt')
    # rectangle obstacle pos read
    while True:
        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        rect_obs_x.append(float(line))

        line = f2.readline()
        line.strip('\n')
        if line == 'end\n' or not line or line == '':
            break
        rect_obs_y.append(float(line))

        line = f2.readline()
        line.strip('\n')
        if line == 'end\n' or not line or line == '':
            break
        rect_obs_size.append(float(line))

        line = f2.readline()
        line.strip('\n')
        if line == 'end\n' or not line or line == '':
            break
        rect_obs_mode.append(int(line))

        rect_obses.append(
            rectangle_obstacle_class.RECTANGLE_OBSTCLE(rect_obs_x[len(rect_obs_x) - 1], rect_obs_y[len(rect_obs_y) - 1],
                                                       rect_obs_size[len(rect_obs_size) - 1],rect_obs_mode[len(rect_obs_mode)-1]))

    f.close()
    f2.close()


def InputGame_Speed():
    background.game_speed = speed
    rectangle_obstacle_class.game_speed = speed
    tile_class.game_speed = speed


def InputGame_SpeedORCamera_Moveing_Degree():
    background.GetGame_Speed(inspeed*game_framework.frame_time)
    for tile in tiles:
        tile.GetCamera_Moving_Degree(camera_x)
    for rect_obstacle in rect_obses:
        rect_obstacle.GetCamera_Moving_Degree(camera_x)
