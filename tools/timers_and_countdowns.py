import os
import pygame
from glumtar import COLUMBIA_BLUE, COUNTDOWN_TIME, FONT, FONT_SIZE, FPS, HEIGHT, WIDTH


class ScrollBG:
    def __init__(self, start=3600):
        self.start = start
        self.accumulate_starts = {'start': self.start}

    def set_bg_timer(self):
        return self.accumulate_starts.get('start')


class CountDown:
    count_top = 6
    count_min = 0
    timer_secs = COUNTDOWN_TIME

    def __init__(self, clock):
        self.clock = clock
        self.initial_time = pygame.time.get_ticks()

        self.range = range
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.pos_X = WIDTH/2
        self.pos_Y = HEIGHT/2
        self.init_value = self.count_top - 1
        self.reset = False
        self.init_value_str = str(self.init_value)
        self.init_value_text = self.font_style.render(
            self.init_value_str, True, COLUMBIA_BLUE)

    def set_countdown(self, screen):
        current_time = pygame.time.get_ticks()
        time_passed = current_time-self.initial_time
        self.init_value_str = str(self.init_value)
        self.init_value_text = self.font_style.render(
            self.init_value_str, True, COLUMBIA_BLUE)

        if time_passed >= self.timer_secs:
            self.init_value -= 1
            self.initial_time = current_time
            screen.blit(self.init_value_text, (self.pos_X, self.pos_Y))

    def reset_countdown(self):
        if self.init_value < 0:
            self.init_value = self.count_top - 1
            self.reset = True
            return self.reset

        # print("He pasado por", time_passed, self.init_value)
