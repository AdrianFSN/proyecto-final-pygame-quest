import os
import random

import pygame

from . import HEIGHT, WIDTH, MARGIN


class Ship(pygame.sprite.Sprite):
    margin = 70
    default_speed = 5
    speed = default_speed
    size_modifier = 4
    speed_boost = 1.7

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

        self.rect = self.img_new_size.get_rect(midleft=(self.margin, HEIGHT/2))

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
            if self.rect.top < 0:
                self.rect.top = 0

        if pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.speed += self.speed_boost
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
        self.reset_speed()


class Meteorite(pygame.sprite.Sprite):
    SPEED = 5
    SIZE_MODIFIER_MAX = 6
    SIZE_MODIFIER_MIN = 2
    SIZE_CONTROLLER = random.randint(SIZE_MODIFIER_MIN, SIZE_MODIFIER_MAX - 1)
    METEORITE_IMG = ['meteorite0_0.png',
                     'meteorite1_0.png', 'meteorite2_0.png']
    ROTATION_SPEED = 2

    def __init__(self, posX=WIDTH):
        super().__init__()
        self.positionX = posX
        self.positionY = random.randint(MARGIN, HEIGHT)
        self.assing_costume()
        self.resize_meteorites()

        self.rotating_meteorite = self.img_new_size
        self.rotation_angle = 0

    def assing_costume(self):
        index = random.randint(0, len(self.METEORITE_IMG)-1)
        for image in self.METEORITE_IMG:
            img_route = os.path.join(
                'glumtar', 'resources', 'images', f'meteorite{index}_0.png')

        self.image = pygame.image.load(img_route)

    def resize_meteorites(self):
        self.image_n_width = self.image.get_width(
        )/(self.SIZE_MODIFIER_MAX - self.SIZE_CONTROLLER)
        self.image_n_height = self.image.get_height(
        )/(self.SIZE_MODIFIER_MAX - self.SIZE_CONTROLLER)

        self.img_new_size = pygame.transform.scale(
            self.image, (self.image_n_width, self.image_n_height))

        self.rect = self.img_new_size.get_rect(
            midright=(self.positionX, self.positionY))
        if self.positionY > HEIGHT - self.image_n_height/2:
            self.positionY = HEIGHT - self.rect.bottom

    def update(self):
        self.rect.x -= self.SPEED
        if self.rect.right < 0:
            return True, print("El mono ha salido")

        if self.rect.right > 0:
            self.rotation_angle += self.ROTATION_SPEED
            self.rotating_meteorite = pygame.transform.rotate(
                self.img_new_size, self.rotation_angle)
