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
        self.is_jump = False
        self.moving_degree, self.game_speed = 0, 0

    def Jump(self):
        self.y += self.jumping_velocity
        self.jumping_velocity -= 0.3
        if self.jumping_velocity < 0:
            self.is_jump, self.jumping_velocity = False, 7
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

    def Fall(self):
        for tile in self.tiles:
            if tile.left + 10 < self.right < tile.right - 10:
                if tile.bottom <= self.bottom <= tile.top + 5:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    return
            elif tile.left + 10 <= self.left <= tile.right < self.right:
                if tile.bottom <= self.bottom <= tile.top + 5:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    return
        self.y += self.falling_velocity
        self.falling_velocity -= 0.2
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

    def draw(self):
        self.image.clip_draw(0, 0, 117, 118, 130, self.y, self.size, self.size)

    def update(self):
        self.Move()
        for tile in self.tiles:
            if self.CheckDeath(tile):
                if self.is_death:
                    return
        for triangle in self.triangle_obstacles:
            self.ColisionCheckWithTriangleObstcles(triangle)
            if self.is_death:
                return

    def Move(self):
        self.x = self.moving_degree + 130
        self.left, self.right = self.x - self.size / 2, self.x + self.size / 2
        if self.is_jump:
            self.Jump()
        else:
            self.Fall()

    def ChangeIsJump(self):
        self.is_jump = True

    def ColisionCheckWithTile(self, tile):
        if self.left >= tile.right:
            return False
        if self.right <= tile.left:
            return False
        if self.top <= tile.bottom:
            return False
        if self.bottom >= tile.top:
            return False
        return True

    def ColisionCheckWithTriangleObstcles(self, triangle):
        if triangle.x - triangle.size / 2 > self.moving_degree - triangle.size and triangle.x + triangle.size < self.moving_degree + 1020:
            dist = (self.x - triangle.x) * (self.x - triangle.x) + (self.y - triangle.y) * (self.y - triangle.y)
            if dist < (self.size / 2 + triangle.size / 2) * (self.size / 2 + triangle.size / 2):
                self.is_death = True
            else:
                self.is_death = False
        return False

    def CheckDeath(self, tile):
        if tile.left > self.moving_degree - tile.size_x and tile.right < self.moving_degree + 1020:
            if self.ColisionCheckWithTile(tile):
                if not tile.top - 3 <= self.bottom:
                    self.is_death = True
        return

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.moving_degree = camera_moving_degree
