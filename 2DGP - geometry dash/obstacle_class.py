from pico2d import*

class OBSTACLE_TRIANGLE:
    image = None
    def __init__(self,x,y):
        if OBSTACLE_TRIANGLE.image == None:
            OBSTACLE_TRIANGLE.image = load_image('triangle_obstacle.png')
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

    def ColideCheck(self, character):
        if (self.x > (-self.size / 2) and self.x < (1000 + self.x / 2)):
            dist = (character.x - self.x)*(character.x-self.x) + (character.y-self.y)*(character.y-self.y)
            if(dist<(character.size/2+self.size/2)*(character.size/2+self.size/2)):
                return True
            else:
                return False
        return False
