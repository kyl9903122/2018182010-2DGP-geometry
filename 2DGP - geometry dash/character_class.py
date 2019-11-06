from pico2d import *
import main_state
import tile_class

class CHARACTER:
    def __init__(self):
        self.image = load_image('character.png')
        self.x, self.y = 130, 500
        self.size = 50
        self.jumping_velocity, self.falling_velocity, self.is_death = 7, 0, False
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2, self.y - self.size / 2, self.x - self.size / 2, self.x + self.size / 2
        self.tiles = []
        self.triangle_obstacles = []
        self.is_death
        self.moving_degree, self.game_speed = 0,0

    def Jump(self):
        self.y += self.jumping_velocity
        self.jumping_velocity -= 0.3
        if self.jumping_velocity < 0:
            self.is_death, self.jumping_velocity = False, 7
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

    def Fall(self):
        for tile in self.tiles:
            if tile.left + 10 < self.right < tile.right - 10:
                if self.bottom <= tile.top:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    return
            elif tile.left + 10 <= self.left <= tile.right < self.right:
                if self.bottom <= tile.top:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    return
        self.y += self.falling_velocity
        self.falling_velocity -= 0.2
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 117, 118, 130, self.y, self.size, self.size)
        pass

    def update(self):
        self.Move()
        for tile in self.tiles:
            if self.CheckDeath(tile):
                self.is_death = True
        for triangle in self.triangle_obstacles:
            self.ColisionCheckWithTriangleObstcles(triangle)


    def Move(self):
        self.x = self.moving_degree
        self.left, self.right = self.x - self.size / 2, self.x + self.size / 2
        if not self.is_death:
            self.Fall()
        if self.is_death:
            self.Jump()

    def ChangeIsJump(self):
        self.is_death = True

    def ColisionCheckWithTile(self,tile):
        if self.left <= tile.right:
            return False
        if self.right >= tile.left:
            return False
        if self.top >= tile.bottom:
            return False
        if self.bottom <= tile.top:
            return False
        return True

    def ColisionCheckWithTriangleObstcles(self,triangle):
        if (-triangle.size / 2) < triangle.x < (1000 + triangle.x / 2):
            dist = (self.x - triangle.x) * (self.x - triangle.x) + (self.y - triangle.y) * (self.y - triangle.y)
            if dist < (self.size / 2 + triangle.size / 2) * (self.size / 2 + triangle.size / 2):
                self.is_death = True
            else:
                self.is_death = False
        return False

    def CheckDeath(self, tile):
        if -tile.size_x / 2 < tile.x < 1000 + tile.size_y:
            if self.ColisionCheckWithTile(tile):
                if self.bottom < tile.bottom:
                    return True
                else:
                    return False
        return False

    def GetCamera_Moving_Degree(self,camera_moving_degree):
        self.moving_degree = camera_moving_degree
