import game_framework
import main_state

name = "MaptoolState"

from pico2d import*

import background_class
import tile_class
import obstacle_class

background = None
home = None
mode, kind = 0,0
tile_x, tile_y, tile_mode, tri_obs_x, tri_obs_y = [], [],[],[],[]
x, y, mx, my, size_x,size_y = 0,0,0,0,0,0
image = None
speed, inspeed, temp_speed = 0.28, 0,0
stop = True
tiles, tri_obses = [] , []
camera_moving_degree_x =0
delete_idx = 0
down_p_count = 0


def enter():
    global mode, kind
    mode = 't'
    kind = 1
    global tile_x, tile_y, tri_obs_x, tri_obs_y
    tile_x, tile_y, tile_mode, tri_obs_x, tri_obs_y = [], [], [], [], []
    global image
    image = load_image('basic_tile.png')

    global x, y, mx, my, size_x,size_y, camera_moving_degree_x, stop
    size_x = 100
    size_y = 100
    camera_moving_degree_x = 0
    stop = True

    global background, speed,inspeed
    background = background_class.BACKGROUND()
    speed= 2.8
    inspeed = 0

    global tiles, tri_obses, delete_idx
    delete_idx = "tile"

    ReadPos()
    pass


def exit():
    # 모드를 나갈때 txt파일에 각 장애물, 타일의 pos값을 저장한다.
    f = open('tile_pos.txt', mode='wt')
    for i in range(len(tiles)):
        f.write(str(tile_x[i]))
        f.write('\n')
        f.write(str(tile_y[i]))
        f.write('\n')
        f.write(str(tile_mode[i]))
        f.write('\n')
    f.write('end\n')

    f2 = open('triangle_obstacle_pos.txt', mode = 'wt')
    for i in range(0,len(tri_obses)):
        f2.write(str(tri_obs_x[i]))
        f2.write('\n')
        f2.write(str(tri_obs_y[i]))
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
    global image, size_x, size_y, mx,my,x,y, inspeed, stop, mode, kind, down_p_count, temp_speed, speed
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if(event.key == SDLK_t):
                # tile selection
                mode = 't'
                if(kind ==1):
                    image = load_image('basic_tile.png')
                    size_x = 100
                    size_y = 100
                elif(kind == 2):
                    image = load_image('tile2.png')
                    size_x = 70
                    size_y = 20
                elif(kind == 3):
                    image = load_image('tile3.png')
                    size_x,size_y = 70,20
            if event.key == SDLK_o:
                # obstacle selection
                mode = 'o'
                if(kind == 1):
                    image = load_image('triangle_obstacle.png')
                    size_x = 40
                    size_y = 40
            if(event.key == SDLK_1):
                kind = 1
                if(mode == 't'):
                    image = load_image('basic_tile.png')
                    size_x =100
                    size_y = 100
                elif(mode == 'o'):
                    image = load_image('triangle_obstacle.png')
                    size_x = 40
                    size_y =40
            if event.key == SDLK_2:
                kind = 2
                if(mode == 't'):
                    image = load_image('tile2.png')
                    size_x = 70
                    size_y = 20
            if event.key == SDLK_3:
                kind = 3
                if(mode == 't'):
                    image = load_image('tile3.png')
                    size_x, size_y = 70, 20
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
                game_framework.change_state(main_state)
            if event.key == SDLK_p:
                down_p_count += 1
                if down_p_count % 2 == 1:
                    temp_speed = speed
                    speed = 10
                else:
                    speed = temp_speed
                    temp_speed = 0
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x = event.x
            y = 510-event.y -1
            Create()
        elif event.type == SDL_MOUSEMOTION:
            mx = event.x
            my = 510 - event.y -1


    pass


def update():
    global speed, camera_moving_degree_x, inspeed,speed
    if(stop == False):
        InputGame_SpeedORCamera_Moveing_Degree()
        InputGame_Speed()
        background.Move()
        speed += 0.0001
        inspeed = speed
        camera_moving_degree_x += inspeed
    delay(0.01)
    pass


def draw():
    hide_cursor()
    clear_canvas()
    background.draw()
    image.draw(mx,my,size_x,size_y)
    for tile in tiles:
        tile.draw()
    for tri_obs in tri_obses:
        tri_obs.draw()
    update_canvas()

    pass

def Create():
    global delete_idx
    if mode == 't' and kind == 1:
        #basic tile
        tiles.append(tile_class.TILE(x,y,size_x,size_y,1))
        tile_x.append(x + camera_moving_degree_x)
        tile_y.append(y)
        tile_mode.append(1)
        delete_idx = "tile"
    elif mode == 't' and kind ==2:
        #tile2
        tiles.append(tile_class.TILE(x , y, size_x, size_y, 2))
        tile_x.append(x + camera_moving_degree_x)
        tile_y.append(y)
        tile_mode.append(2)
        delete_idx = "tile"
    elif mode == 't' and kind == 3:
        # tile3
        tiles.append(tile_class.TILE(x, y, size_x, size_y, 3))
        tile_x.append(x + camera_moving_degree_x)
        tile_y.append(y)
        tile_mode.append(3)
        delete_idx = "tile"
    elif mode == 'o' and kind == 1:
        #triangle obstacle
        tri_obses.append(obstacle_class.OBSTACLE_TRIANGLE(x,y))
        tri_obs_x.append(x + camera_moving_degree_x)
        tri_obs_y.append(y)
        delete_idx = "tri_obs"


    pass

def DeleteBlock():
    if(delete_idx =="tile"):
        del tiles[len(tiles)-1]
        del tile_x[len(tiles)-1]
        del tile_y[len(tiles)-1]
        del tile_mode[len(tile_mode)-1]

    if(delete_idx == "tri_obs"):
        del tri_obses[len(tri_obses)-1]
        del tri_obs_y[len(tri_obs_y)-1]
        del tri_obs_x[len(tri_obs_x)-1]
    pass

def ReadPos():
    global tile_x,tile_y,tile_mode,tri_obs_x,tri_obs_y,tiles,tri_obses
    f = open('tile_pos.txt',mode = 'rt')
    #tile pos read
    while True:
        line = f.readline()
        line.strip('\n')
        if line == 'end\n' or (not line) or line == '':
            break
        tile_x.append(float(line))
        line = f.readline()
        line.strip('\n')
        if  line == 'end\n' or (not line) or line == '':
            break
        tile_y.append(float(line))
        line = f.readline()
        line.strip('\n')
        if  line == 'end\n' or not line or line == '':
            break
        tile_mode.append(int(line))
        if tile_mode[len(tile_mode)-1] == 1:
            tiles.append(tile_class.TILE(tile_x[len(tile_x)-1],tile_y[len(tile_x)-1],100,100,1))
        elif tile_mode[len(tile_mode)-1] == 2:
            tiles.append(tile_class.TILE(tile_x[len(tile_x)-1],tile_y[len(tile_y)-1],70,20,2))
        elif tile_mode[len(tile_mode)-1] == 3:
            tiles.append(tile_class.TILE(tile_x[len(tile_x) - 1], tile_y[len(tile_y) - 1], 70, 20, 3))



    f2 = open('triangle_obstacle_pos.txt', mode='rt')
    #triangle obstacle pos read
    while True:
        line = f2.readline()
        line.strip('\n')
        if line == "end\n" or not line or line == '':
            break
        tri_obs_x.append(float(line))

        line = f2.readline()
        line.strip('\n')
        if  line == 'end\n' or not line or line == '':
            break
        tri_obs_y.append(float(line))

        tri_obses.append(obstacle_class.OBSTACLE_TRIANGLE(tri_obs_x[len(tri_obs_x)-1],tri_obs_y[len(tri_obs_y)-1]))

    f.close()
    f2.close()

def InputGame_Speed():
    background.game_speed = speed
    obstacle_class.game_speed = speed
    tile_class.game_speed = speed



def InputGame_SpeedORCamera_Moveing_Degree():
    background.GetGame_Speed(inspeed)
    for tile in tiles:
        tile.GetCamera_Moving_Degree(camera_moving_degree_x)
    for triangle_obstacle in tri_obses:
        triangle_obstacle.GetCamera_Moving_Degree(camera_moving_degree_x)