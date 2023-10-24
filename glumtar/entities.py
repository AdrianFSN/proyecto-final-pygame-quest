import os
import random

import pygame

from . import COLUMBIA_BLUE, FONT, FONT_SIZE, HEIGHT, LIVES, LIVES_MARGIN, TOP_MARGIN_LIMIT, HEARTS_MARGIN, METEO_OUTER_MARGIN, SCOREBOARD_MARGIN, WIDTH


class Ship(pygame.sprite.Sprite):
    left_margin = 70
    default_speed = 0
    speed = default_speed
    speed_boost = .5

    def __init__(self):
        super().__init__()
        self.img_route = os.path.join(
            'glumtar', 'resources', 'images', 'ship0_0.png')
        self.image = pygame.image.load(self.img_route)
        self.rect = self.image.get_rect(
            midleft=(self.left_margin, (HEIGHT + TOP_MARGIN_LIMIT)/2))

        # self.expl_frame = 1

        self.explosion_frames = {}
        for index in range(1, 61):
            self.explosion_img_route = os.path.join(
                'glumtar', 'resources', 'images', 'explosion_frames', f'explosion{index}.png')
            self.explosion_frames[index] = self.explosion_img_route

    def explode_the_ship(self, amount):
        amount = amount
        # for self.expl_frame in self.explosion_frames:
        if amount <= 60:
            self.image = pygame.image.load(
                self.explosion_frames.get(amount))
            print(
                f"He pintado la imagen {self.explosion_frames.get(amount)}")
        # amount += 1

    # def change_frame(self):
        # self.expl_frame += 1

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
            if self.rect.top < TOP_MARGIN_LIMIT:
                self.rect.top = TOP_MARGIN_LIMIT
        self.reset_speed()

        if pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.speed += self.speed_boost
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
        self.reset_speed()


class Meteorite(pygame.sprite.Sprite):
    default_speed = 7
    default_points = 1
    outer_margin = WIDTH + METEO_OUTER_MARGIN
    meteorite_img = ['meteorite0_0.png',
                     'meteorite1_0.png', 'meteorite2_0.png']
    speed_family_0 = default_speed
    speed_family_1 = default_speed + 2.5
    speed_family_2 = default_speed + 5.5
    points_family_0 = default_points
    points_family_1 = default_points * 2
    points_family_2 = default_points * 3

    def __init__(self, speed=default_speed, points=default_points, posX=outer_margin):
        super().__init__()
        self.speed = speed
        self.points = points
        self.positionX = posX
        self.positionY = random.randint(TOP_MARGIN_LIMIT, HEIGHT)
        self.assing_family()

    def assing_family(self):
        index = random.randint(0, len(self.meteorite_img)-1)
        for image in self.meteorite_img:
            img_route = os.path.join(
                'glumtar', 'resources', 'images', f'meteorite{index}_0.png')

        if 'meteorite1_' in img_route:
            self.speed = self.speed_family_1
            self.points = self.points_family_1

        elif 'meteorite2_' in img_route:
            self.speed = self.speed_family_2
            self.points = self.points_family_2

        self.image = pygame.image.load(img_route)
        self.rect = self.image.get_rect(
            midright=(self.positionX, self.positionY))

    def update(self):
        self.rect.x -= self.speed
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < TOP_MARGIN_LIMIT:
            self.rect.top = TOP_MARGIN_LIMIT


class Scoreboard:
    margin_title = 50
    font_title_adjust = 20

    def __init__(self, points=0):
        self.scoreboard_value = points
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)

    def increase_score(self, score_up):
        self.scoreboard_value += score_up

    def show_scoreboard(self, screen):
        score_string = str(self.scoreboard_value)
        scoreboard_text = self.font_style.render(
            score_string, True, COLUMBIA_BLUE)
        pointsX = SCOREBOARD_MARGIN
        pointsY = TOP_MARGIN_LIMIT - FONT_SIZE
        screen.blit(scoreboard_text, (pointsX, pointsY))


class LivesCounter:
    def __init__(self, lives=LIVES):
        self.lives_value = lives
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.available_lives = {}
        self.livesX = WIDTH - LIVES_MARGIN
        self.livesY = TOP_MARGIN_LIMIT - FONT_SIZE
        self.decrease_lives = 1

        self.end_game = False

        for index in range(1, LIVES + 1):
            hearts_route = os.path.join(
                'glumtar', 'resources', 'images', f'lives{index}.png')
            self.available_lives[index] = hearts_route

        self.hearts_image = pygame.image.load(
            self.available_lives.get(self.lives_value))
        self.heartsX = WIDTH - HEARTS_MARGIN
        self.heartsY = TOP_MARGIN_LIMIT - (self.hearts_image.get_height()/2)
        self.rect = self.hearts_image.get_rect(
            midright=(self.heartsX, self.heartsY))

    def show_lives(self, screen):
        if self.lives_value > 0:
            self.hearts_image = pygame.image.load(
                self.available_lives.get(self.lives_value))
            lives_string = str(self.lives_value)
            lives_text = self.font_style.render(
                lives_string, True, COLUMBIA_BLUE)
            screen.blit(lives_text, (self.livesX, self.livesY))
            screen.blit(self.hearts_image, self.rect)
            return False
        else:
            return True

    def reduce_lives(self, collision):
        collision = collision
        if collision:
            if self.lives_value >= 1:
                self.lives_value -= self.decrease_lives
                collision = False
                return collision
            else:
                collision = False
                return collision
