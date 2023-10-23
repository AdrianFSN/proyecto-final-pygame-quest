import os
import pygame
from glumtar import COLUMBIA_BLUE, FONT, FONT_SIZE, FONT_SIZE_CONTROLLER, HEIGHT, WIDTH


class ScrollBG:
    def __init__(self, start=3600):
        self.start = start
        self.accumulate_starts = {'start': self.start}

    def set_bg_timer(self):
        return self.accumulate_starts.get('start')


class Countdown:

    def __init__(self, screen, start=3, stop=0):
        self.start = start
        self.counter = self.start
        self.stop = stop
        self.screen = screen

        font = FONT
        font_size = FONT_SIZE + FONT_SIZE_CONTROLLER
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, font_size)
        self.pos_X = WIDTH/2
        self.pos_Y = HEIGHT/2

        self.reset = False

    def draw_countdown(self):
        if self.counter >= self.stop:
            counter_str = str(self.counter)
            counter_text = self.font_style.render(
                counter_str, True, COLUMBIA_BLUE)
            self.screen.blit(counter_text, (self.pos_X, self.pos_Y))

    def discount_countdown(self):
        self.counter -= 1

    def reset_countdown(self):
        # self.counter = self.stop
        self.counter = self.start
