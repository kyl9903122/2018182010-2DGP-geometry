from pico2d import *
import game_framework

GET_OFF_POS = 8900

MOUSE_DOWN, MOUSE_UP, INVIHINCLE_KEY, FINISH_STAGE, MOVE_START, REVERSE, GET_OFF_UFO = range(7)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None): MOUSE_DOWN,
    (SDL_MOUSEBUTTONUP, None): MOUSE_UP,
    (SDL_KEYDOWN, SDLK_p): INVIHINCLE_KEY
}


class Stop_State:
    @staticmethod
    def enter(ufo, event):
        if  event == INVIHINCLE_KEY:
            if ufo.no_death:
                ufo.no_death = False
                print("ufo invi: ", ufo.no_death)
            else:
                ufo.no_death = True
                print("ufo invi: ", ufo.no_death)
        pass

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        if ufo.move:
            ufo.add_event(MOVE_START)
        pass

    @staticmethod
    def draw(ufo):
        ufo.image.draw(ufo.x - ufo.camera_moving_degree, ufo.y, ufo.size_x, ufo.size_y)


class Fly_State:
    @staticmethod
    def enter(ufo, event):
        if event == MOUSE_DOWN:
            ufo.fly = True
            ufo.velocity = 0
        elif event == MOUSE_UP:
            ufo.fly = False
            ufo.velocity = 0
        elif event == INVIHINCLE_KEY:
            if ufo.no_death:
                ufo.no_death = False
                print("ufo invi: ", ufo.no_death)
            else:
                ufo.no_death = True
                print("ufo invi: ", ufo.no_death)
        pass

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        ufo.x = ufo.camera_moving_degree + 130
        ufo.left, ufo.right = ufo.x - ufo.size_x / 2, ufo.x + ufo.size_x / 2
        if ufo.fly:
            print("ufo up")
            ufo.Up()
        else:
            print("ufo down")
            ufo.Fall()
        if not ufo.no_death:
            for obstacle in ufo.obstacles:
                if ufo.ColideCheck(obstacle):
                    print("collide ufo: ", ufo.x, " ", obstacle.x)
                    ufo.collide = True
                    break
            if ufo.bottom <= 0:
                ufo.collide = True
        if len(ufo.REVERSE_POS) > 0:
            if ufo.left >= ufo.REVERSE_POS[0]:
                del ufo.REVERSE_POS[0]
                print(ufo.REVERSE_POS)
                ufo.add_event(REVERSE)
        if ufo.x >= GET_OFF_POS:
            ufo.add_event(GET_OFF_UFO)

    @staticmethod
    def draw(ufo):
        ufo.image.draw(130, ufo.y, ufo.size_x, ufo.size_y)


class Reverse_Fly_State:
    @staticmethod
    def enter(ufo, event):
        if event == MOUSE_DOWN:
            ufo.fly = True
            ufo.velocity = 0
        elif event == MOUSE_UP:
            ufo.fly = False
            ufo.velocity = 0
        elif event == INVIHINCLE_KEY:
            if ufo.no_death:
                ufo.no_death = False
                print("ufo invi: ", ufo.no_death)
            else:
                ufo.no_death = True
                print("ufo invi: ", ufo.no_death)

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        ufo.x = ufo.camera_moving_degree + 130
        ufo.left, ufo.right = ufo.x - ufo.size_x / 2, ufo.x + ufo.size_x / 2
        if ufo.fly:
            print("ufo up")
            ufo.Down()
        else:
            print("ufo down")
            ufo.Up()
        if not ufo.no_death:
            for obstacle in ufo.obstacles:
                if ufo.ColideCheck(obstacle):
                    print("collide ufo: ", ufo.x, " ", obstacle.x)
                    ufo.collide = True
                    break
            if ufo.top >= 510:
                ufo.collide = True
        if len(ufo.REVERSE_POS) > 0:
            if ufo.left >= ufo.REVERSE_POS[0]:
                del ufo.REVERSE_POS[0]
                ufo.add_event(REVERSE)
        if ufo.x >= GET_OFF_POS:
            ufo.add_event(GET_OFF_UFO)

    @staticmethod
    def draw(ufo):
        ufo.image.composite_draw(0, 'v', 130, ufo.y, ufo.size_x, ufo.size_y)


class Disapear_State:
    @staticmethod
    def enter(ufo, event):
        if event == INVIHINCLE_KEY:
            if ufo.no_death:
                ufo.no_death = False
                print("ufo invi: ", ufo.no_death)
            else:
                ufo.no_death = True
                print("ufo invi: ", ufo.no_death)

    @staticmethod
    def exit(ufo, event):
        pass

    @staticmethod
    def do(ufo):
        pass

    @staticmethod
    def draw(ufo):
        ufo.image.draw(130, ufo.y, ufo.size_x, ufo.size_y)

next_state_table = {
    Stop_State: {MOUSE_DOWN: Stop_State, MOUSE_UP: Stop_State, INVIHINCLE_KEY: Stop_State, FINISH_STAGE: Stop_State,
                 MOVE_START: Fly_State, REVERSE: Stop_State,GET_OFF_UFO: Stop_State},
    Fly_State: {MOUSE_DOWN: Fly_State, MOUSE_UP: Fly_State, INVIHINCLE_KEY: Fly_State, FINISH_STAGE: Stop_State,
                MOVE_START: Fly_State, REVERSE: Reverse_Fly_State, GET_OFF_UFO: Disapear_State},
    Reverse_Fly_State: {MOUSE_DOWN: Reverse_Fly_State, MOUSE_UP: Reverse_Fly_State, INVIHINCLE_KEY: Reverse_Fly_State,
                        FINISH_STAGE: Stop_State, MOVE_START: Reverse_Fly_State, REVERSE: Fly_State, GET_OFF_UFO: Disapear_State},
    Disapear_State: {MOUSE_DOWN: Disapear_State, MOUSE_UP: Disapear_State, INVIHINCLE_KEY: Disapear_State,
                        FINISH_STAGE: Disapear_State, MOVE_START: Disapear_State, REVERSE: Disapear_State, GET_OFF_UFO: Disapear_State}
}


class UFO:
    def __init__(self):
        self.image = load_image('UFO.png')
        self.x, self.y, self.size_x, self.size_y, = 1000, 126, 90, 50
        self.obstacles, self.tiles = [], []
        # 충돌체크시 필요한 bound box를 만든다
        self.top, self.bottom, self.left, self.right = self.y + self.size_y / 2, self.y - self.size_y / 2, self.x - self.size_x / 2, self.x + self.size_x / 2
        self.camera_moving_degree = 0
        self.REVERSE_POS = [4589.568407440174, 7119.122155946479, 7598.9953683554995,8242.51725965538]
        # 캐릭터가 UFO를 타면 True가 된다
        self.move = False
        self.fly = False
        self.collide = False
        self.no_death = False
        self.velocity = 0
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
        self.Down()
        for tile in self.tiles:
            if self.ColideCheck(tile):
                self.y = tile.top + self.size_y / 2
                self.velocity = 0

    def Up(self):
        self.y -= self.velocity * game_framework.frame_time
        self.velocity -= 15
        self.top, self.bottom = self.y + self.size_y / 2, self.y - self.size_y / 2

    def Down(self):
        self.y += self.velocity * game_framework.frame_time
        self.velocity -= 15
        self.top, self.bottom = self.y + self.size_y / 2, self.y - self.size_y / 2
