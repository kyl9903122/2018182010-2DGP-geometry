from pico2d import *
import game_framework
import Change_Stage_state

GET_OFF_POS = 8900

# Character Event
MOUSE_DOWN, MOUSE_UP, INVIHINCLE_KEY, FINISH_STAGE, RIDE_UFO, REVERSE, GET_OFF_UFO = range(7)

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
            if character.jumping_cnt < 2:
                character.is_jump = True
            character.jumping_cnt += 1
            character.angle = (character.angle - 90) % 360
        elif event == INVIHINCLE_KEY:
            if character.no_death:
                character.no_death = False
            else:
                character.no_death = True
        elif event == GET_OFF_UFO:
            character.size = 50
            character.ride_ufo = False
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.Move()
        if not character.no_death:
            for tile in character.tiles:
                if character.CheckDeath(tile):
                    if character.is_death:
                        return
            for triangle in character.obstacles:
                character.ColisionCheckWithTriangleObstcles(triangle)
                if character.is_death:
                    return
        if character.x >= character.GOAL_POINT:
            # del GOAL_POINT[0]
            character.add_event(FINISH_STAGE)
        if character.ride_ufo:
            character.add_event(RIDE_UFO)

    @staticmethod
    def draw(character):
        if character.map_stop:
            character.image.clip_draw(0, 0, 117, 118, character.x - (character.GOAL_POINT - 694) + 130, character.y,
                                      character.size,
                                      character.size)
        else:
            character.image.composite_draw(character.angle / 360 * 2 * math.pi,'',130, character.y, character.size, character.size)


################################################################################################################

class Stop_State:
    @staticmethod
    def enter(character, event):
        if event == FINISH_STAGE:
            character.is_jump = True
            character.jumping_velocity = 800
            character.falling_velocity = 0
            character.success_sound.play()
        global timer
        timer = 2
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        global timer
        timer -= game_framework.frame_time
        if timer <= 0:
            game_framework.change_state(Change_Stage_state)
            character.success_sound.stop()
        if character.is_jump:
            if character.stage == 3:
                character.Reverse_Jump()
            else:
                character.Jump()
        else:
            if character.stage == 3:
                character.Reverse_Fall()
                if character.top >= 410:
                    character.y = 410 - character.size / 2
                    character.y = 410 - character.size / 2
                    character.is_jump = True
                    character.falling_velocity = 0
                    character.jumping_velocity = 800
            else:
                character.Fall()
                if character.bottom <= 100:
                    character.y = 100 + character.size / 2
                    character.y = 100 + character.size / 2
                    character.is_jump = True
                    character.falling_velocity = 0
                    character.jumping_velocity = 800

    @staticmethod
    def draw(character):
        if character.stage == 3:
            character.image.composite_draw(0, 'hv', character.x, character.y,
                                           character.size, character.size)
        else:
            character.image.clip_draw(0, 0, 117, 118, character.x - (character.GOAL_POINT - 694) + 130, character.y,
                                      character.size, character.size)


##########################################################################################################################

class Fly_State:
    @staticmethod
    def enter(character, event):
        print("character fly enter")
        if event == RIDE_UFO:
            character.size = 40
            character.y = character.ufo.y + 35
        elif event == INVIHINCLE_KEY:
            if character.no_death:
                character.no_death = False
            else:
                character.no_death = True

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.x = character.moving_degree + 130
        character.left, character.right = character.x - character.size / 2, character.x + character.size / 2
        character.y = character.ufo.y + 35
        character.top, character.bottom = character.y + character.size / 2, character.y - character.size / 2
        if not character.no_death:
            for obstacle in character.obstacles:
                if character.ColisionCheckWithTile(obstacle):
                    character.is_death = True
                    break
            if character.top >= 510:
                character.is_death = True
        if len(character.REVERSE_POS) > 0:
            if character.left >= character.REVERSE_POS[0]:
                del character.REVERSE_POS[0]
                character.add_event(REVERSE)
        if character.x >= GET_OFF_POS:
            character.add_event(GET_OFF_UFO)

    @staticmethod
    def draw(character):
        character.image.clip_draw(0, 0, 200, 200, 130, character.y, character.size, character.size)


#####################################################################################################################

class Reverse_Fly_State:
    @staticmethod
    def enter(character, event):
        print("character reverse fly enter")
        if event == RIDE_UFO:
            character.size = 40
            character.y = character.ufo.y - 35
        elif event == INVIHINCLE_KEY:
            if character.no_death:
                character.no_death = False
            else:
                character.no_death = True

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.x = character.moving_degree + 130
        character.left, character.right = character.x - character.size / 2, character.x + character.size / 2
        character.y = character.ufo.y - 35
        character.top, character.bottom = character.y + character.size / 2, character.y - character.size / 2
        if not character.no_death:
            for obstacle in character.obstacles:
                if character.ColisionCheckWithTile(obstacle):
                    character.is_death = True
                    break
            if character.top <= 0:
                character.is_death = True
        if len(character.REVERSE_POS) > 0:
            if character.left >= character.REVERSE_POS[0]:
                del character.REVERSE_POS[0]
                character.add_event(REVERSE)
        if character.x >= GET_OFF_POS:
            character.add_event(GET_OFF_UFO)

    @staticmethod
    def draw(character):
        character.image.composite_draw(0, 'v', 130, character.y, character.size, character.size)


############################################################################################################################

class Reverse_Run_State:
    @staticmethod
    def enter(character, event):
        if event == MOUSE_DOWN:
            character.is_jump = True
        elif event == INVIHINCLE_KEY:
            if character.no_death:
                character.no_death = False
            else:
                character.no_death = True
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        character.Reverse_Move()
        if not character.no_death:
            for tile in character.tiles:
                # check die
                if tile.left > character.moving_degree - tile.size_x and tile.right < character.moving_degree + 1020:
                    if character.ColisionCheckWithTile(tile):
                        if tile.mode == 3:
                            character.is_death = True
                        if tile.top < character.top:
                            character.is_death = True
                    if character.y >= 510:
                        character.is_death = True
                    if character.is_death:
                        return
            for triangle in character.obstacles:
                character.ColisionCheckWithTriangleObstcles(triangle)
                if character.is_death:
                    return
        if character.x <= character.GOAL_POINT:
            character.add_event(FINISH_STAGE)

    @staticmethod
    def draw(character):
        if character.map_stop:
            print("character.x: ", character.x)
            character.image.composite_draw(0, 'hv', character.x, character.y, character.size, character.size)
        else:
            character.image.composite_draw(0, 'hv', 1020 - 130, character.y, character.size, character.size)


next_state_table = {
    Run_State: {MOUSE_DOWN: Run_State, MOUSE_UP: Run_State, INVIHINCLE_KEY: Run_State, FINISH_STAGE: Stop_State,
                RIDE_UFO: Fly_State, REVERSE: Run_State, GET_OFF_UFO: Run_State},
    Fly_State: {MOUSE_DOWN: Fly_State, MOUSE_UP: Fly_State, INVIHINCLE_KEY: Fly_State, FINISH_STAGE: Stop_State,
                RIDE_UFO: Fly_State, REVERSE: Reverse_Fly_State, GET_OFF_UFO: Run_State},
    Stop_State: {MOUSE_DOWN: Stop_State, MOUSE_UP: Stop_State, INVIHINCLE_KEY: Stop_State, FINISH_STAGE: Stop_State,
                 RIDE_UFO: Stop_State, REVERSE: Stop_State, GET_OFF_UFO: Stop_State},
    Reverse_Fly_State: {MOUSE_DOWN: Reverse_Fly_State, MOUSE_UP: Reverse_Fly_State, INVIHINCLE_KEY: Reverse_Fly_State,
                        FINISH_STAGE: Stop_State, RIDE_UFO: Reverse_Fly_State, REVERSE: Fly_State,
                        GET_OFF_UFO: Run_State},
    Reverse_Run_State: {MOUSE_DOWN: Reverse_Run_State, MOUSE_UP: Reverse_Run_State, INVIHINCLE_KEY: Reverse_Run_State,
                        FINISH_STAGE: Stop_State, RIDE_UFO: Reverse_Run_State, REVERSE: Reverse_Run_State,
                        GET_OFF_UFO: Reverse_Run_State}
}


class CHARACTER:
    def __init__(self):
        self.image = load_image('character.png')
        self.x, self.y = 130, 500
        self.size = 50
        self.jumping_velocity, self.falling_velocity, self.is_death = 800, 0, False
        self.map_stop = 0
        self.top, self.bottom, self.left, self.right = self.y + self.size / 2, self.y - self.size / 2, self.x - self.size / 2, self.x + self.size / 2
        self.tiles = []
        self.obstacles = []
        self.is_jump = False
        self.moving_degree = 0
        self.no_death = False
        self.ufo = None
        self.fly = False
        self.ride_ufo = False
        self.event_que = []
        self.cur_state = Run_State
        self.cur_state.enter(self, None)
        self.REVERSE_POS = [3793.651009301344, 5618.495640911652, 7305.081099476411, 8069.334514486767]
        self.GOAL_POINT = 0
        self.stage = 0
        self.jumping_cnt = 0
        self.success_sound = load_music("success.wav")
        self.angle = 0

    def Jump(self):
        self.y += self.jumping_velocity * game_framework.frame_time
        self.jumping_velocity -= 11
        self.falling_velocity = 0

        if self.jumping_velocity < 0:
            print(self.jumping_velocity)
            self.is_jump, self.jumping_velocity = False, 800
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

    def Reverse_Jump(self):
        self.y -= self.jumping_velocity * game_framework.frame_time
        self.jumping_velocity -= 8
        if self.jumping_velocity < 0:
            self.is_jump, self.jumping_velocity = False, 800
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2

    def Fall(self):
        self.Down()
        for tile in self.tiles:
            if tile.left + 5 < self.right < tile.right - 5:
                if tile.bottom <= self.bottom <= tile.top + 2:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    self.jumping_cnt = 0
                    return
            elif tile.left + 5 <= self.left <= tile.right < self.right:
                if tile.bottom <= self.bottom <= tile.top + 2:
                    self.y = tile.top + self.size / 2
                    self.falling_velocity = 0
                    self.jumping_cnt = 0
                    return

    def Reverse_Fall(self):
        self.y -= self.falling_velocity * game_framework.frame_time
        self.falling_velocity -= 5
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2
        for tile in self.tiles:
            if self.ColisionCheckWithTile(tile):
                if tile.top >= self.top >= tile.bottom - 2:
                    self.y = tile.bottom - self.size / 2
                    self.falling_velocity = 0
                    self.jumping_cnt = 0

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

    def Move(self):
        self.x = self.moving_degree + 130
        self.left, self.right = self.x - self.size / 2, self.x + self.size / 2
        if self.is_jump:
            self.Jump()
        else:
            self.Fall()

    def Reverse_Move(self):
        self.x = self.moving_degree + 1020 - 130
        self.left, self.right = self.x - self.size / 2, self.x + self.size / 2
        if self.is_jump:
            self.Reverse_Jump()
        else:
            self.Reverse_Fall()

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

    def Down(self):
        self.y += self.falling_velocity * game_framework.frame_time
        self.falling_velocity -= 5
        self.top, self.bottom = self.y + self.size / 2, self.y - self.size / 2
