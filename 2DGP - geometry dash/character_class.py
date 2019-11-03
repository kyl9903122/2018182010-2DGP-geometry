from pico2d import*
import main_state
import tile_class

degree = 0

class CHARACTER:
    def __init__(self):
        self.image = load_image('character.png')
        self.x, self.y = 130, 130
        self.size = 50
        global velocity,dir, fall
        velocity = 7
        fall = -2
        dir = 1
        self.top, self.bottom, self.left, self.right = self.y + self.size/2, self.y - self.size/2, self.x-self.size/2, self.x+self.size/2
        global isJump
        isJump = False

    def Jump(self,tiles):
        global velocity, dir, isJump
        self.y += velocity
        velocity -= 0.3
        if(velocity < 0):
            for tile in tiles:
                if (self.left>=tile.left and self.right < tile.right):
                    if (self.bottom-3<= tile.top+3):
                           self.y = tile.top + self.size/2
                           isJump = False
                           velocity = 7
                    elif self.left>= tile.left + 10 and self.right > tile.right:
                       if (self.bottom - 3 <= tile.top + 3):
                           self.y = tile.top + self.size / 2
                           isJump = False
                           velocity = 7
                    elif self.right >= tile.left+10 and self.left<tile.left:
                       if (self.bottom - 3 <= tile.top + 3):
                           self.y = tile.top + self.size / 2
                           isJump = False
                           velocity = 7
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2, self.y - self.size / 2, self.x - self.size / 2, self.x + self.size / 2


    def Fall(self,tiles):
        global fall
        for tile in tiles:
            if (self.left >= tile.left and self.right < tile.right):
                if (self.bottom - 3 <= tile.top + 3):
                    self.y = tile.top - self.size / 2
                    return
            elif self.left >= tile.left + 10 and self.right > tile.right:
                if (self.bottom - 3 <= tile.top + 3):
                    self.y = tile.top - self.size / 2
                    return
            elif self.right >= tile.left + 10 and self.left < tile.left:
                if (self.bottom - 3 <= tile.top + 3):
                    self.y = tile.top - self.size / 2
                    return
        self.y -= fall
        fall -=1
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2, self.y - self.size / 2, self.x - self.size / 2, self.x + self.size / 2
        pass



    def Draw(self):
        self.image.clip_draw(0, 0, 117, 118, self.x, self.y, self.size, self.size)
        pass

    def Move(self,tiles):
        if(isJump == False):
            Fall(tiles)
        if(isJump == True):
            Jump(tiles)