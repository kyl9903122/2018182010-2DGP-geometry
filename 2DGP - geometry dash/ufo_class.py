from pico2d import*
import game_framework

MOUSE_DOWN, MOUSE_UP, INVIHINCLE_KEY, FINISH_STAGE, MOVE_START, REVERSE = range(6)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None): MOUSE_DOWN,
    (SDL_MOUSEBUTTONUP, None): MOUSE_UP,
    (SDL_KEYDOWN, SDLK_p): INVIHINCLE_KEY
}

class Stop_State:
    @staticmethod
    def enter(ufo, event):
        pass

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        pass

    @staticmethod
    def draw(ufo):
        ufo.image.draw(ufo.x - ufo.camera_moving_degree, ufo.y, ufo.size_x, ufo.size_y)

class Fly_State:
    @staticmethod
    def enter(ufo, event):
        pass

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        ufo.x = ufo.moving_degree + 130
        if ufo.fly:
            ufo.
        pass

    @staticmethod
    def draw(ufo):
        ufo.image.draw(130, ufo.y, ufo.size_x, ufo.size_y)


class Reverse_Fly_State:
    @staticmethod
    def enter(ufo, event):
        pass

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        ufo.x = ufo.moving_degree + 130
        pass

    @staticmethod
    def draw(ufo):
        ufo.image.composite_draw(0,'v',130, ufo.y, ufo.size_x, ufo.size_y)


next_state_table = {
    Stop_State: {MOUSE_DOWN: Stop_State, MOUSE_UP: Stop_State, INVIHINCLE_KEY: Stop_State, FINISH_STAGE: Stop_State, MOVE_START: Fly_State, REVERSE: Stop_State},
    Fly_State: {MOUSE_DOWN: Fly_State, MOUSE_UP: Fly_State, INVIHINCLE_KEY: Fly_State, FINISH_STAGE: Stop_State, MOVE_START: Fly_State,REVERSE:Reverse_Fly_State},
    Reverse_Fly_State: {MOUSE_DOWN: Reverse_Fly_State, MOUSE_UP: Reverse_Fly_State, INVIHINCLE_KEY: Reverse_Fly_State, FINISH_STAGE: Stop_State,MOVE_START: Reverse_Fly_State,REVERSE:Fly_State}
}


class UFO:
    def __init__(self):
        self.image = load_image('UFO.png')
        self.x, self.y, self.size_x, self.size_y,= 1000, 110, 50,20
        self.obstacles,self.tiles = [],[]
        # 충돌체크시 필요한 bound box를 만든다
        self.top, self.bottom, self.left, self.right = self.y + self.size_y / 2, self.y - self.size_y / 2, self.x - self.size_x / 2, self.x + self.size_x / 2
        self.camera_moving_degree = 0
        # 캐릭터가 UFO를 타면 True가 된다
        self.move = False
        self.fly = False
        self.event_que = []
        self.cur_state = Stop_State
        self.cur_state.enter(self, None)

    def draw(self):
        self.cur_state.draw(self)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def GetCamera_Moving_Degree(self, camera_moving_degree):
        self.camera_moving_degree = camera_moving_degree

    def ColideCheck(self, obstacle):
        if self.left > obstacle.right:
            return False
        if self.right < obstacle.left + 2:
            return False
        if self.top < obstacle.bottom:
            return False
        if self.bottom > obstacle.top:
            return False
        return True

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