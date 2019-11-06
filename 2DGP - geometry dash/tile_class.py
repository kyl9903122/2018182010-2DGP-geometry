from pico2d import *


class TILE:
    game_speed = 0
    def __init__(self, x, y, size_x, size_y, mode):
        # mode에 따라 타일의 모양이 달라진다. 1. basic tile
        self.image = None
        if mode == 1:
            self.image = load_image('basic_tile.png')
        elif mode == 2:
            self.image = load_image('tile2.png')
        self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y
        # 충돌체크시 필요한 bound box를 만든다
        self.top, self.bottom, self.left, self.right = self.y + self.size_y / 2, self.y - self.size_y / 2, self.x - self.size_x / 2, self.x + self.size_x / 2

    def Move(self):
        if self.x > -self.size_x / 2:
            self.x -= self.game_speed
            self.left, self.right = self.x - self.size_x / 2, self.x + self.size_x / 2

    def draw(self):
        if -self.size_x / 2 < self.x < 1000 + self.size_x / 2:
            self.image.draw(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        self.Move()

