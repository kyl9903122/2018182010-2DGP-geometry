from pico2d import *
import game_framework

# Character Event
MOUSE_DOWN, MOUSE_UP, INVIHINCLE_KEY = range(3)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None): MOUSE_DOWN,
    (SDL_MOUSEBUTTONUP, None): MOUSE_UP,
    (SDL_KEYDOWN, SDLK_p): INVIHINCLE_KEY
}


class State1_State:
    @staticmethod
    def enter(character, event):
        if event == MOUSE_DOWN:
            character.is_jump = True
        elif event == INVIHINCLE_KEY:
            if character.invincicle_mode:
                character.invincicle_mode = False
            else:
                character.invincicle_mode = True
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        print("State1 State do")
        character.Move()
        if not character.invincicle_mode:
            for tile in character.tiles:
                if character.CheckDeath(tile):
                    if character.is_death:
                        return
            for triangle in character.triangle_obstacles:
                character.ColisionCheckWithTriangleObstcles(triangle)
                if character.is_death:
                    return
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(0, 0, 117, 118, 130, character.y, character.size, character.size)
        pass


next_state_table = {
    State1_State: {MOUSE_DOWN: State1_State, MOUSE_UP: State1_State, INVIHINCLE_KEY: State1_State}
}


class CHARACTER:
    def __init__(self):
        self.image = load_image('character.png')
        self.x, self.y = 130, 500
        self.size = 50
        self.jumping_velocity, self.falling_velocity, self.is_death = 650, 0, False
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2, self.y - self.size / 2, self.x - self.size / 2, self.x + self.size / 2
        self.tiles = []
        self.triangle_obstacles = []
        self.is_jump = False
        self.moving_degree, self.game_speed = 0, 0
        self.invincicle_mode = False
        self.event_que = []
        self.cur_state = State1_State
        self.cur_state.enter(self, None)


    def Jump(self):
        self.y += self.jumping_velocity * game_framework.frame_time
        self.jumping_velocity -= 30
        if self.jumping_velocity < 0:
            self.is_jump, self.jumping_velocity = False, 650
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

    def Fall(self):
        self.y += self.falling_velocity * game_framework.frame_time
        self.falling_velocity -= 15
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2
        for tile in self.tiles:
            if tile.left + 5 < self.right < tile.right - 5:
                if tile.bottom <= self.bottom <= tile.top + 2:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    return
            elif tile.left + 5 <= self.left <= tile.right < self.right:
                if tile.bottom <= self.bottom <= tile.top + 2:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    return

    def draw(self):
        self.cur_state.draw(self)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self,event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)

    def add_event(self,event):
        self.event_que.insert(0,event)

    def handle_event(self,event):
        if(event.type,event.key) in key_event_table:
            key_event = key_event_table[(event.type,event.key)]
            self.add_event(key_event)


    def Move(self):
        self.x = self.moving_degree + 130
        self.left, self.right = self.x - self.size / 2, self.x + self.size / 2
        if not self.invincicle_mode:
            if self.is_jump:
                self.Jump()
            else:
                self.Fall()

    def ColisionCheckWithTile(self, tile):
        if self.left > tile.right:
            return False
        if self.right < tile.left + 2:
            return False
        if self.top < tile.bottom:
            return False
        if self.bottom > tile.top:
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
                if tile.mode == 3:
                    self.is_death = True
                    print("die for tile mode 3")
                if tile.bottom > self.bottom:
                    self.is_death = True
                    print("die for collision with tile")
                    print(self.bottom, self.bottom)
            if self.y <= 0:
                self.is_death = True

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.moving_degree = camera_moving_degree

