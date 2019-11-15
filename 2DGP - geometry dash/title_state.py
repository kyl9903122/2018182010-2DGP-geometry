import game_framework
from pico2d import *
import State1_state


name = "TitleState"
image = None


def enter():
    global image
    image = load_image('title2.png')
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
                game_framework.change_state(State1_state)
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





