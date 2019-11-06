from pico2d import *


class TILE:
    game_speed = 0
    image_1 = None
    image_2 = None
    def __init__(self, x, y, size_x, size_y, mode):
        # mode에 따라 타일의 모양이 달라진다. 1. basic tile
        self.image = None
        if TILE.image_1 == None:
           TILE.image_1 = load_image('basic_tile.png')
        if TILE.image_2 == None:
            TILE.image_2 = load_image('tile2.png')
        self.x, self.y, self.size_x, self.size_y,self.mode = x, y, size_x, size_y, mode
        # 충돌체크시 필요한 bound box를 만든다
        self.top, self.bottom, self.left, self.right = self.y + self.size_y / 2, self.y - self.size_y / 2, self.x - self.size_x / 2, self.x + self.size_x / 2
        self.camera_moving_degree = 0

    def draw(self):
        if self.left>=self.camera_moving_degree-self.size_x and self.right<=self.camera_moving_degree+1020+self.size_x:
            if self.mode == 1:
                TILE.image_1.draw(self.x-self.camera_moving_degree, self.y, self.size_x, self.size_y)
            else:
                TILE.image_2.draw(self.x-self.camera_moving_degree, self.y, self.size_x, self.size_y)

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.camera_moving_degree = camera_moving_degree

