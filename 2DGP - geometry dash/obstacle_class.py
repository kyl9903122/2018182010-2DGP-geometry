from pico2d import*

class OBSTACLE_TRIANGLE:
    def __init__(self,x,y):
        self.image = load_image('triangle_obstacle.png')
        self.x, self.y, self.size = x, y, 40
        self.speed = 2.8
        pass

    def Move(self, speed):
        if (self.x > (-self.size / 2)):
            self.x -= speed
        pass

    def Draw(self):
        if (self.x > (-self.size / 2) and self.x < (1000 + self.x / 2)):
            self.image.draw(self.x,self.y,self.size,self.size)
        pass

    def ColideCheck(self, character_x, character_y, character_size):
        if (self.x > (-self.size / 2) and self.x < (1000 + self.x / 2)):
            dist = (character_x - self.x)*(character_x-self.x) + (character_y-self.y)*(character_y-self.y)
            if(dist<(character_size/2+self.size/2)*(character_size/2+self.size/2)):
                return True
            else:
                return False
        return False
