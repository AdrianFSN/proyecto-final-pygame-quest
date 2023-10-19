import os
import pygame
from glumtar import COLUMBIA_BLUE, DEFAULT_TIMER, FONT, FONT_SIZE, FPS, HEIGHT, WIDTH


class Timer:
    def __init__(self, start=3600):
        self.start = start
        self.accumulate_starts = {'start': self.start}

    def set_timer(self):

        return self.accumulate_starts.get('start')


class CountDown:
    count_top = 6
    count_min = 0
    countdown_range = (count_min, count_top)
    timer_secs = 1000

    def __init__(self, clock, timer, range=countdown_range):
        self.clock = clock
        self.timer = timer
        self.initial_time = pygame.time.get_ticks()

        self.range = range
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.pos_X = WIDTH/2
        self.pos_Y = HEIGHT/2
        self.init_value = self.count_top - 1

    def set_count_down(self, screen):
        current_time = pygame.time.get_ticks()
        time_passed = current_time-self.initial_time
        init_value_str = str(self.init_value)
        init_value_text = self.font_style.render(
            init_value_str, True, COLUMBIA_BLUE)
        screen.blit(init_value_text, (self.pos_X, self.pos_Y))

        if time_passed >= self.timer_secs:
            self.init_value -= 1
            self.initial_time = current_time

        print("He pasado por", time_passed, self.init_value)
