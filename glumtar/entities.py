import os
import random

import pygame

from . import COLUMBIA_BLUE, FONT, FONT_SIZE, HEIGHT, MARGIN, SCOREBOARD_HEIGHT, SCOREBOARD_MARGIN, SCOREBOARD_WIDTH, WIDTH


class Ship(pygame.sprite.Sprite):
    left_margin = 70
    default_speed = 0
    speed = default_speed
    size_modifier = 4
    speed_boost = .5

    def __init__(self):
        super().__init__()
        img_route = os.path.join(
            'glumtar', 'resources', 'images', 'ship0_0.png')
        self.image = pygame.image.load(img_route)
        self.resize_ship()

    def resize_ship(self):
        self.image_n_width = self.image.get_width()/self.size_modifier
        self.image_n_height = self.image.get_height()/self.size_modifier

        self.img_new_size = pygame.transform.scale(
            self.image, (self.image_n_width, self.image_n_height))

        self.rect = self.img_new_size.get_rect(
            midleft=(self.left_margin, (HEIGHT + MARGIN)/2))

    def reset_speed(self):
        self.pressed = pygame.key.get_pressed()
        self.pressed_up = self.pressed[pygame.K_UP]
        self.pressed_down = self.pressed[pygame.K_DOWN]
        if not self.pressed_up and not self.pressed_down:
            self.speed = self.default_speed
            return self.speed

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            self.speed += self.speed_boost
            if self.rect.top < MARGIN:
                self.rect.top = MARGIN
        self.reset_speed()

        if pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.speed += self.speed_boost
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
        self.reset_speed()


class Meteorite(pygame.sprite.Sprite):
    DEFAULT_SPEED = 7
    DEFAULT_POINTS = 1
    SIZE_MODIFIER_MAX = 5
    SIZE_MODIFIER_MIN = 1
    SIZE_CONTROLLER = random.randint(SIZE_MODIFIER_MIN, SIZE_MODIFIER_MAX)
    OUTER_MARGIN = 150
    METEORITE_IMG = ['meteorite0_0.png',
                     'meteorite1_0.png', 'meteorite2_0.png']
    SPEED_FAMILY_0 = DEFAULT_SPEED
    SPEED_FAMILY_1 = DEFAULT_SPEED + 2.5
    SPEED_FAMILY_2 = DEFAULT_SPEED + 5.5
    POINTS_FAMILY_0 = DEFAULT_POINTS
    POINTS_FAMILY_1 = DEFAULT_POINTS * 2
    POINTS_FAMILY_2 = DEFAULT_POINTS * 3

    def __init__(self, speed=DEFAULT_SPEED, points=DEFAULT_POINTS, posX=WIDTH + OUTER_MARGIN):
        super().__init__()
        self.speed = speed
        self.points = points
        self.positionX = posX
        self.positionY = random.randint(MARGIN, HEIGHT)
        self.assing_family()

    def assing_family(self):
        index = random.randint(0, len(self.METEORITE_IMG)-1)
        for image in self.METEORITE_IMG:
            img_route = os.path.join(
                'glumtar', 'resources', 'images', f'meteorite{index}_0.png')

        if 'meteorite1_' in img_route:
            self.speed = self.SPEED_FAMILY_1
            self.points = self.POINTS_FAMILY_1

        elif 'meteorite2_' in img_route:
            self.speed = self.SPEED_FAMILY_2
            self.points = self.POINTS_FAMILY_2

        self.image = pygame.image.load(img_route)
        self.rect = self.image.get_rect(
            midright=(self.positionX, self.positionY))

    def update(self):
        self.rect.x -= self.speed
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < MARGIN:
            self.rect.top = MARGIN


class Scoreboard:
    margin_title = 50
    font_title_adjust = 20

    def __init__(self, points=0):
        self.scoreboard_value = points
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.scoreboard_title = 'PUNTOS'

    def increase_score(self, score_up):
        self.scoreboard_value += score_up

    def show_scoreboard(self, screen):
        score_string = str(self.scoreboard_value)
        scoreboard_text = self.font_style.render(
            score_string, True, COLUMBIA_BLUE)
        pointsX = SCOREBOARD_MARGIN
        pointsY = SCOREBOARD_HEIGHT
        screen.blit(scoreboard_text, (pointsX, pointsY))
