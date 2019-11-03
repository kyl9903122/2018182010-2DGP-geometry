from pico2d import*

class BACKGROUND:
    def __init__(self):
        self.image_1 = load_image('background1.png')
        self.image_2 = load_image('background1.png')
        self.image_3 = load_image('background1.png')
        self.pivot_1_x, self.pivot_2_x, self.pivot_3_x = 255, 765, 1275
        self.pivot_y = 255

    def Move(self, speed):
        if (self.pivot_1_x <= -255):
            self.pivot_1_x = self.pivot_3_x + 510
        if (self.pivot_2_x <= -255):
            self.pivot_2_x = self.pivot_1_x + 510
        if (self.pivot_3_x <= -255):
            self.pivot_3_x = self.pivot_2_x + 510
        self.pivot_1_x -= speed
        self.pivot_2_x -= speed
        self.pivot_3_x -= speed

    def Draw(self):
        self.image_1.clip_draw(0, 0, 512, 512, self.pivot_1_x, self.pivot_y, 512, 512)
        self.image_2.clip_draw(0, 0, 512, 512, self.pivot_2_x, self.pivot_y, 512, 512)
        self.image_3.clip_draw(0, 0, 512, 512, self.pivot_3_x, self.pivot_y, 512, 512)