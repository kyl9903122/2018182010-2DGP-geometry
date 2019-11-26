import game_framework
from pico2d import *
import Stage2_state
import Stage3_state
import finish_state

name = "Change Stage"
image = None
next_stage = 0


def enter():
    global image
    image = load_image('change_stage.png')
    game_framework.cur_stage += 1
    if game_framework.cur_stage == 4:
        game_framework.change_state(finish_state)
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
                if game_framework.cur_stage == 2:
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
