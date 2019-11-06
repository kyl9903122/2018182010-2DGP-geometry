from pico2d import*

class BACKGROUND:
    def __init__(self):
        self.image_1 = load_image('background1.png')
        self.image_2 = load_image('background1.png')
        self.image_3 = load_image('background1.png')
        self.pivot_1_x, self.pivot_2_x, self.pivot_3_x = 255, 765, 1275
        self.pivot_y = 255
        self.bgm = load_music("Geomatry_resource_backmusic.mp3")
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.game_speed = 0

    def Move(self):
        if (self.pivot_1_x <= -255):
            self.pivot_1_x = self.pivot_3_x + 510
        if (self.pivot_2_x <= -255):
            self.pivot_2_x = self.pivot_1_x + 510
        if (self.pivot_3_x <= -255):
            self.pivot_3_x = self.pivot_2_x + 510
        self.pivot_1_x -= self.game_speed
        self.pivot_2_x -= self.game_speed
        self.pivot_3_x -= self.game_speed

    def draw(self):
        self.image_1.clip_draw(0, 0, 512, 512, self.pivot_1_x, self.pivot_y, 512, 512)
        self.image_2.clip_draw(0, 0, 512, 512, self.pivot_2_x, self.pivot_y, 512, 512)
        self.image_3.clip_draw(0, 0, 512, 512, self.pivot_3_x, self.pivot_y, 512, 512)

    def update(self):
        self.Move()
