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
        pass

    def Move(self, speed):
        if(self.x>-self.size_x/2):
            self.x -= speed
        pass

    def Draw(self):
        if(self.x>-self.size_x/2 and self.x<1000+self.size_x/2):
            self.image.draw(self.x,self.y,self.size_x,self.size_y)
        pass

    def ColideCheck(self,character_x,character_y,character_size):
        left,right,top,bottom = self.x - self.size_x/2,self.x+self.size_x/2,self.y+self.size_y/2,self.y-self.size_y/2
        character_left,character_right,character_top,character_bottom = character_x-character_size/2,character_x+character_size/2,character_y+character_size/2,character_y-character_size/2
        if(left>=character_right):
            return False
        if(right<=character_left):
            return False
        if top<=character_bottom:
            return False
        if bottom>=character_top:
            return False
        return True
        pass

    def CheckDie(self,character_x,character_y,character_size):
        left, right, top, bottom = self.x - self.size_x / 2, self.x + self.size_x / 2, self.y + self.size_y / 2, self.y - self.size_y / 2
        character_left, character_right, character_top, character_bottom = character_x - character_size / 2, character_x + character_size / 2, character_y + character_size / 2, character_y - character_size / 2
        if self.x>-self.size_x/2 and self.x<1000+self.size_y:
            if(self.ColideCheck(character_x,character_y,character_size)):
                if(character_bottom<top):
                    return "die"
                else:
                    self.y = tile_top + self.size / 2
                    return "put"
        return "none"
        pass