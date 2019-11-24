from pico2d import *


class OBSTACLE_TRIANGLE:
    image = None
    game_speed = 2.8

    def __init__(self, x, y):
        if OBSTACLE_TRIANGLE.image is None:
            OBSTACLE_TRIANGLE.image = load_image('triangle_obstacle.png')
        self.x, self.y, self.size = x, y, 40
        self.camera_moving_degree = 0
        self.stage = 1

    def draw(self):
        if self.stage == 3:
            if (self.x-self.size/2 > self.camera_moving_degree-self.size and self.x + self.size/2):
                self.image.comsite_draw(0,'v',self.x-self.camera_moving_degree, self.y, self.size, self.size)
        else:
            if (self.x-self.size/2 > self.camera_moving_degree-self.size and self.x + self.size/2):
                self.image.draw(self.x-self.camera_moving_degree, self.y, self.size, self.size)

    def update(self):
        pass

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.camera_moving_degree = camera_moving_degree
