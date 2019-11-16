from pico2d import *
import game_framework
import title_state

import Stage2_state

GOAL1_POINT = 7190
WORD1_END_X = 7440.704599999951


# Character Event
MOUSE_DOWN, MOUSE_UP, INVIHINCLE_KEY, FINISH_STAGE, RIDE_VIHICLE = range(5)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None): MOUSE_DOWN,
    (SDL_MOUSEBUTTONUP, None): MOUSE_UP,
    (SDL_KEYDOWN, SDLK_p): INVIHINCLE_KEY
}

###################################################################################################

class Run_State:
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
        if character.x >= GOAL1_POINT:
            character.cur_state = Stop_State
            character.cur_state.enter(character,FINISH_STAGE)
        if character.x >= VIHICLE_START_POINT:
            character.cur_state = Fly_State
            character.cur_state.enter(character,RIDE_VIHICLE)
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
        if character.map_stop:
            character.image.clip_draw(0, 0, 117, 118, character.x - 6541 + 130, character.y, character.size,
                                      character.size)
        else:
            character.image.clip_draw(0, 0, 117, 118, 130, character.y, character.size, character.size)

################################################################################################################

class Stop_State:
    @staticmethod
    def enter(character, event):
        if event == FINISH_STAGE:
            character.is_jump = True
            character.jumping_velocity = 400
            character.falling_velocity = 0
        global timer
        timer = 3
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        global timer
        timer -= game_framework.frame_time
        if timer <= 0:
            if timer <= 0:
                game_framework.change_state(Stage2_state)
        if character.is_jump:
            character.Jump()
            character.jumping_velocity = 400
        else:
            character.Fall()
            if character.bottom <= 100:
                character.y = 100 + character.size / 2
                character.y = 100 + character.size / 2
                character.is_jump = True
                character.falling_velocity = 0

    @staticmethod
    def draw(character):
        character.image.clip_draw(0, 0, 117, 118, character.x - 6541 + 130, character.y, character.size, character.size)

##########################################################################################################################

class Fly_State:
    @staticmethod
    def enter(character, event):
        print("Fly_State")
        if event == RIDE_VIHICLE:
            character.size = 40
        global timer
        timer = 3

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        global timer
        timer -= game_framework.frame_time
        if timer <= 0:
            game_framework.change_state(Stage2_state)
        if character.is_jump:
            character.Jump()
        else:
            character.jumping_velocity = 400
            character.Fall()
            if character.bottom <= 100:
                character.y = 100 + character.size / 2
                character.is_jump = True
                character.falling_velocity = 0

    @staticmethod
    def draw(character):
        character.image.clip_draw(0, 0, 200, 200, 130, character.y, character.size, character.size)


next_state_table = {
    Run_State: {MOUSE_DOWN: Run_State, MOUSE_UP: Run_State, INVIHINCLE_KEY: Run_State, FINISH_STAGE: Stop_State, RIDE_VIHICLE: Fly_State},
    Fly_State: {MOUSE_DOWN: Fly_State, MOUSE_UP: Fly_State, INVIHINCLE_KEY: Fly_State, FINISH_STAGE: Stop_State, RIDE_VIHICLE: Fly_State},
    Stop_State: {MOUSE_DOWN: Stop_State, MOUSE_UP: Stop_State, INVIHINCLE_KEY: Stop_State, FINISH_STAGE: Stop_State, RIDE_VIHICLE: Stop_State}
}


class CHARACTER:
    def __init__(self):
        self.image = load_image('character.png')
        self.x, self.y = 130, 500
        self.size = 50
        self.jumping_velocity, self.falling_velocity, self.is_death = 650, 0, False
        self.map_stop = 0
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2, self.y - self.size / 2, self.x - self.size / 2, self.x + self.size / 2
        self.tiles = []
        self.triangle_obstacles = []
        self.is_jump = False
        self.moving_degree= 0
        self.invincicle_mode = False
        self.ufo = None
        self.event_que = []
        self.cur_state = Run_State
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

    def Fall_Reverse(self):
        self.y -= self.falling_velocity * game_framework.frame_time
        self.falling_velocity -= 15
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

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
                if tile.bottom > self.bottom:
                    self.is_death = True
                    print(self.bottom, self.bottom)
            if self.y <= 0:
                self.is_death = True

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.moving_degree = camera_moving_degree

