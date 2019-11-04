from pico2d import*
import main_state
import tile_class

degree = 0

class CHARACTER:
    def __init__(self):
        self.image = load_image('character.png')
        self.x, self.y = 130, 500
        self.size = 50
        self.velocity, self.fall, self.isJump = 7, 0, False
        self.top, self.bottom, self.left, self.right = self.y + self.size/2, self.y - self.size/2, self.x-self.size/2, self.x+self.size/2

    def Jump(self,tiles):
        self.y += self.velocity
        self.velocity -= 0.3
        print("jump:")
        print(self.y)
        if(self.velocity < 0):
            self.isJump, self.velocity = False, 7
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2


    def Fall(self,tiles):
        for tile in tiles:
            if self.right > tile.left +10 and self.right < tile.right-10:
                if self.bottom <= tile.top:
                    self.y = tile.top + self.size/2
                    self.fall = 0
                    return
            elif self.left >= tile.left+10 and self.left <= tile.right and tile.right < self.right:
                if self.bottom <= tile.top:
                    self.y = tile.top + self.size / 2
                    self.fall = 0
                    return
        self.y += self.fall
        self.fall -=0.2
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2
        pass



    def Draw(self):
        self.image.clip_draw(0, 0, 117, 118, self.x, self.y, self.size, self.size)
        pass

    def Move(self,tiles):
        if(self.isJump == False):
            self.Fall(tiles)
        if(self.isJump == True):
            self.Jump(tiles)

    def ChangeIsJump(self):
        self.isJump = True
        print(self.isJump)