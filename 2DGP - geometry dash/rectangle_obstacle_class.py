from pico2d import *


class RECTANGLE_OBSTCLE:
    game_speed = 0
    image_1 = None
    image_2 = None
    image_3 = None
    image_4 = None
    image_5 = None
    gate_image = None

    def __init__(self, x, y, size, mode):
        # mode에 따라 타일의 모양이 달라진다. 1. basic tile
        if RECTANGLE_OBSTCLE.image_1 is None:
            RECTANGLE_OBSTCLE.image_1 = load_image('Rect_Obstacle100x100.png')
        if RECTANGLE_OBSTCLE.image_2 is None:
            RECTANGLE_OBSTCLE.image_2 = load_image('Rect_Obstacle150x150.png')
        if RECTANGLE_OBSTCLE.image_3 is None:
            RECTANGLE_OBSTCLE.image_3 = load_image('Rect_Obstacle200x200.png')
        if RECTANGLE_OBSTCLE.image_4 is None:
            RECTANGLE_OBSTCLE.image_4 = load_image('Rect_Obstacle250x250.png')
        if RECTANGLE_OBSTCLE.image_5 is None:
            RECTANGLE_OBSTCLE.image_5 = load_image('Rect_Obstacle300x300.png')
        if RECTANGLE_OBSTCLE.gate_image is None:
            RECTANGLE_OBSTCLE.gate_image = load_image('Reverse_Gate.png')
        self.x, self.y, self.size, self.mode = x, y, size, mode
        # 충돌체크시 필요한 bound box를 만든다
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2 -3, self.y - self.size / 2 +3, self.x - self.size /  +3, self.x + self.size / 2 -3
        self.camera_moving_degree = 0

    def draw(self):
        if self.left >= self.camera_moving_degree - self.size and self.right <= self.camera_moving_degree + 1020 + self.size:
            if self.size == 100 and self.mode == 1:
                RECTANGLE_OBSTCLE.image_1.draw(self.x - self.camera_moving_degree, self.y, self.size, self.size)
            elif self.size == 150 and self.mode == 1:
                RECTANGLE_OBSTCLE.image_2.draw(self.x - self.camera_moving_degree, self.y, self.size, self.size)
            elif self.size == 200 and self.mode == 1:
                RECTANGLE_OBSTCLE.image_3.draw(self.x - self.camera_moving_degree, self.y, self.size, self.size)
            elif self.size == 250 and self.mode == 1:
                RECTANGLE_OBSTCLE.image_4.draw(self.x - self.camera_moving_degree, self.y, self.size, self.size)
            elif self.size == 300 and self.mode == 1:
                RECTANGLE_OBSTCLE.image_5.draw(self.x - self.camera_moving_degree, self.y, self.size, self.size)
            elif self.mode == 2:
                RECTANGLE_OBSTCLE.gate_image.draw(self.x - self.camera_moving_degree, self.y, self.size, self.size)

    def update(self):
        pass

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.camera_moving_degree = camera_moving_degree
