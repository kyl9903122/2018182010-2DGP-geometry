from pico2d import*

class TILE:
    def __init__(self,x,y,size_x,size_y,mode):
        #mode에 따라 타일의 모양이 달라진다. 1. basic tile
        self.image = None
        if(mode == 1):
            self.image = load_image('basic_tile.png')
        elif(mode == 2):
            self.image = load_image('tile2.png')
        self.x, self.y, self.size_x, self.size_y = x,y,size_x,size_y
        self.top, self.bottom, self.left, self.right = self.y + self.size_y/2,self.y-self.size_y/2,self.y+self.size_x/2,self.x-self.size_x/2
        pass

    def Move(self, speed):
        if(self.x>-self.size_x/2):
            self.x -= speed
        pass

    def Draw(self):
        if(self.x>-self.size_x/2 and self.x<1000+self.size_x/2):
            self.image.draw(self.x,self.y,self.size_x,self.size_y)
        pass

    def ColideCheck(self,character):
        if(self.left>=character.right):
            return False
        if(self.right<=character.left):
            return False
        if self.top<=character.bottom:
            return False
        if self.bottom>=character.top:
            return False
        return True
        pass

    def CheckDie(self,character):
        if self.x>-self.size_x/2 and self.x<1000+self.size_y:
            if(self.ColideCheck(character)):
                if(character_bottom<bottom):
                    return "die"
                else:
                    return "put"
        return "none"
        pass