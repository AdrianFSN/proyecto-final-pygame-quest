import os
import random

import pygame

from . import ANIMATION_FRAMES, COLUMBIA_BLUE, FONT, FONT_SIZE, HEIGHT, LIVES, LIVES_MARGIN, TOP_MARGIN_LIMIT, HEARTS_MARGIN, METEO_OUTER_MARGIN, SCOREBOARD_MARGIN, WIDTH


class Ship(pygame.sprite.Sprite):
    left_margin = 70
    default_speed = 0
    speed = default_speed
    speed_boost = .5
    landing_speed = 2
    rotating_speed = 2
    rotation_angle = 10
    pos_ship_after_rotation = (0, 0)

    def __init__(self, screen, land=False):
        super().__init__()
        self.screen = screen
        self.land = land
        self.request_draw_rotation = False

        self.rotated_image = None
        self.rotated_image_rect = None

        self.img_route = os.path.join(
            'glumtar', 'resources', 'images', 'ship0_0.png')
        self.image = pygame.image.load(self.img_route)
        self.rect = self.image.get_rect(
            midleft=(self.left_margin, (HEIGHT + TOP_MARGIN_LIMIT)/2))

        self.explosion_frames = {}
        for index in range(1, ANIMATION_FRAMES):
            self.explosion_img_route = os.path.join(
                'glumtar', 'resources', 'images', 'explosion_frames', f'explosion{index}.png')
            self.explosion_frames[index] = self.explosion_img_route

    def explode_the_ship(self, amount):
        amount = amount
        if amount < ANIMATION_FRAMES:
            self.image = pygame.image.load(
                self.explosion_frames.get(amount))

    def reset_ship_costume(self):
        self.img_route = os.path.join(
            'glumtar', 'resources', 'images', 'ship0_0.png')
        self.image = pygame.image.load(self.img_route)
        self.rect = self.image.get_rect(
            midleft=(self.left_margin, (HEIGHT + TOP_MARGIN_LIMIT)/2))

    def reset_speed(self):
        self.pressed = pygame.key.get_pressed()
        self.pressed_up = self.pressed[pygame.K_UP]
        self.pressed_down = self.pressed[pygame.K_DOWN]
        if not self.pressed_up and not self.pressed_down:
            self.speed = self.default_speed
            return self.speed

    def update(self):
        if not self.land:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] and not pressed[pygame.K_DOWN]:
                self.rect.y -= self.speed
                self.speed += self.speed_boost
                if self.rect.top < TOP_MARGIN_LIMIT:
                    self.rect.top = TOP_MARGIN_LIMIT
            self.reset_speed()

            if pressed[pygame.K_DOWN] and not pressed[pygame.K_UP]:
                self.rect.y += self.speed
                self.speed += self.speed_boost
                if self.rect.bottom > HEIGHT:
                    self.rect.bottom = HEIGHT
            self.reset_speed()
        else:
            self.land_ship()

    def land_ship(self):
        descend_speed = 2
        if self.rect.y < (HEIGHT - self.image.get_height())/2:
            self.rect.y += self.landing_speed
            if self.rect.y >= (HEIGHT - self.image.get_height())/2:
                self.rect.x += self.landing_speed

        elif self.rect.y > (HEIGHT - self.image.get_height())/2:
            self.rect.y -= self.landing_speed
            if self.rect.y == (HEIGHT - self.image.get_height())/2:
                self.rect.x += self.landing_speed

        if self.rect.x >= (WIDTH - self.image.get_width())/2:
            self.landing_speed = 0
        if self.landing_speed == 0:
            self.rotate_ship()

    def rotate_ship(self):
        rotation_center = self.rect.center
        original_image = pygame.image.load(self.img_route)

        if self.rotation_angle < 180:
            self.rotated_image = pygame.transform.rotate(
                original_image, self.rotation_angle)
            self.rotated_image_rect = self.rotated_image.get_rect(
                center=(rotation_center))
            self.screen.blit(self.rotated_image, self.rotated_image_rect)
            self.rotation_angle += self.rotating_speed
            self.request_draw_rotation = True
            self.pos_ship_after_rotation = (
                self.rotated_image_rect.x, self.rotated_image_rect.y)
        else:
            self.rect = self.rotated_image_rect
            self.image = self.rotated_image
            self.request_draw_rotation = False

        return self.request_draw_rotation


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

        for index in range(0, LIVES + 1):
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
        if self.lives_value >= 0:
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
