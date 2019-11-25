import game_framework
from pico2d import *
import Stage1_state
import Stage2_state
import Stage3_state

name = "TitleState"
image = None
cur_stage = 0

def enter():
    global image, cut_stage
    image = load_image('fail.png')
    pass


def exit():
    global image
    del image
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                if game_framework.cur_stage == 1:
                    game_framework.change_state(Stage1_state)
                elif game_framework.cur_stage == 2:
                    game_framework.change_state(Stage2_state)
                elif game_framework.cur_stage == 3:
                    game_framework.change_state(Stage3_state)
            elif event.key == SDLK_ESCAPE:
                game_framework.quit()
    pass


def draw():
    clear_canvas()
    image.draw(510, 255)
    update_canvas()
    pass


def update():

    pass


def pause():
    pass


def resume():
    pass





