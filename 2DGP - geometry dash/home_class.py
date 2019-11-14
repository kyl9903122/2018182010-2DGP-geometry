from pico2d import *

class HOME:
    def __init__(self, x, y):
        self.image = load_image('palg.png')
        self.x, self.y = x,y
        self.camera_moving_degree = 0
        self.size_x, self.size_y = 858,720
        self.left,self.right,self.top,self.bottom = self.x - self.size_x/2, self.x + self.size_x/2,self.y + self.size_y/2, self.y - self.size_y/2

    def draw(self):
        if self.left >= self.camera_moving_degree - self.size_x and self.right <= self.camera_moving_degree + 1020 + self.size_x:
            if self.mode == 1:
                self..image_1.draw(self.x - self.camera_moving_degree, self.y, self.size_x, self.size_y)
            elif self.mode == 2:
                self.image_2.draw(self.x - self.camera_moving_degree, self.y, self.size_x, self.size_y)
            elif self.mode == 3:
                self.image_3.draw(self.x - self.camera_moving_degree, self.y, self.size_x, self.size_y)


    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.camera_moving_degree = camera_moving_degree