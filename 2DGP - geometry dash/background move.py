from pico2d import*
import  math
open_canvas(1020,510)

TILESIZE = 100
TILECNT = 6
CHARACTERSIZE = 50
TRIOBSTACLESIZE = 40
#init

background_1 = load_image('background1.png')
background_2 = load_image('background1.png')
background_3 = load_image('background1.png')
basic_tile = load_image('basic_tile.png')
character = load_image('character.png')
tirangle_obstacle = load_image('triangle_obstacle.png')
tile_2 = load_image('tile2.png')
tiles = [basic_tile,basic_tile,basic_tile,basic_tile,basic_tile,basic_tile,tile_2,tile_2,tile_2]
tile_size = [100,100,100,100,100,100,50,50,50]



background_1_pivotX = 255
background_2_pivotX = 765
background_3_pivotX = 1275
backgroundPivotY = 255
speed = 2.8
character_jump =False

def handle_events():
    global running
    global character_jump
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDL_ESCAPE:
                # 이부분은 이후 일시정지 되도록 바꾼다 -> 추가구현 내용
                running = False
        if event.type == SDL_MOUSEBUTTONDOWN:
            character_jump = True

def BackgroundMove():
    global background_1_pivotX
    global background_2_pivotX
    global background_3_pivotX
    global speed
    if(background_1_pivotX<=-255):
        background_1_pivotX = background_3_pivotX+510
    if(background_2_pivotX<=-255):
        background_2_pivotX = background_1_pivotX+510
    if(background_3_pivotX<=-255):
        background_3_pivotX = background_2_pivotX+510
    background_1_pivotX -= speed    
    background_2_pivotX -= speed
    background_3_pivotX -= speed
   

def BackgroundDraw(bk1_pivot_x,bk2_pivot_x,bk3_pivot_x,bk_pivot_y):
    background_1.clip_draw(0,0,512,512,bk1_pivot_x,bk_pivot_y,512,512)
    background_2.clip_draw(0,0,512,512,bk2_pivot_x,bk_pivot_y,512,512)
    background_2.clip_draw(0,0,512,512,bk3_pivot_x,bk_pivot_y,512,512)
    
def UpSpeed():
    global speed
    speed += 0.0001

def InitMap():
    #초기 단계이므로 일단 타일만 깐다
    global tiles_pivot_x
    global tiles_pivot_y
     # tiles pivot value
    tiles_pivot_x = [50,150,250,350,450,550,700,850,1000]
    tiles_pivot_y= [50,50,50,50,50,50,50,50,50]

def TilesMove():
    for i in range(0,len(tiles)):
        tiles_pivot_x[i] -= speed

def DrawTiles():
    for i in range(0,len(tiles)):
        if(tiles_pivot_x[i]>=-50 and tiles_pivot_y[i]<=1070):
            tiles[i].draw(tiles_pivot_x[i],tiles_pivot_y[i])

def MoveOvstacles():
   global obstacle_x
   global obstacle_y
   for i in range(0,len(obstacle_x)):
       obstacle_x[i]-=speed

def DrawObstacles():
    for i in range(0,len(obstacle_x)):
        if(obstacle_x[i]>-TRIOBSTACLESIZE/2 and obstacle_x[i]<1000+TRIOBSTACLESIZE):
            tirangle_obstacle.clip_draw(0, 0, 50, 50, obstacle_x[i], obstacle_y[i], TRIOBSTACLESIZE, TRIOBSTACLESIZE)

def MoveCharacter():
    global character_x, character_y
    global degree
    if(character_jump == True):
        character_y += math.sin(degree/360 *2 *math.pi) * 4
        degree+=7

def Maptool(m_x,m_y):

    pass

def ColideCheck():
    global colide
    obs_circle = [0,0,0]    # x , y ,r
    cha_circle = [character_x,character_y,CHARACTERSIZE/2]
    for i in range(0,len(obstacle_x)):
        obs_circle = [obstacle_x[i],obstacle_y[i],TRIOBSTACLESIZE/2]
        dist = (cha_circle[0] - obs_circle[0]) * (cha_circle[0] - obs_circle[0]) + (cha_circle[1] - obs_circle[1]) * (
                    cha_circle[1] - obs_circle[1])
        if (obstacle_x[i] > -TRIOBSTACLESIZE/2 and obstacle_x[i] < 1000+TRIOBSTACLESIZE/2):
            if(dist<(obs_circle[2]+cha_circle[2])*(obs_circle[2]+cha_circle[2])):
                colide=True
                break;







running = True
basic_tiles_x = [0 for n in range(0, TILECNT)]
basic_tiles_y = [50 for n in range(0, TILECNT)]
character_x, character_y = 130, 130
obstacle_x = [500, 800,1100,1500,1800]
obstacle_y = [115, 115,115,115,115]
degree = 0
colide = False
fall = False

InitMap()
while(running):
    handle_events()
    #update
    BackgroundMove()
    UpSpeed()
    TilesMove()
    MoveCharacter()
    if ( degree>360):
        degree = 0
        character_y = 130
        character_jump = False
    MoveOvstacles()
    ColideCheck()
    if(colide == True):
        running = False
    #draw
    clear_canvas()
    BackgroundDraw(background_1_pivotX,background_2_pivotX,background_3_pivotX,backgroundPivotY)
    DrawTiles()
    character.clip_draw(0,0,117,118,character_x,character_y,CHARACTERSIZE,CHARACTERSIZE)
    DrawObstacles()

    update_canvas()


    delay(0.01)

