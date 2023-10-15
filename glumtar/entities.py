import os
import random

import pygame

from . import HEIGHT, WIDTH, MARGIN


class Ship(pygame.sprite.Sprite):
    margin = 70
    speed = 5
    size_modifier = 4
    speed_boost = 1.3

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

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.accelerated_speed = self.speed
            self.rect.y -= self.speed + \
                self.accelerate(self.accelerated_speed)
            if self.rect.top < 0:
                self.rect.top = 0

        if pressed[pygame.K_DOWN]:
            self.accelerated_speed = self.speed
            self.rect.y += self.speed + \
                self.accelerate(self.accelerated_speed)
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    def accelerate(self, speed):
        acceleration = speed
        acceleration *= self.speed_boost
        if self.accelerated_speed != self.speed:
            return self.accelerated_speed

        return acceleration


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
