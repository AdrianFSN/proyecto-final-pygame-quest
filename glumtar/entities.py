import os
from typing import Any
import pygame
from . import HEIGHT, WIDTH


class Ship(pygame.sprite.Sprite):
    margin = 50
    speed = 5
    size_modifier = 4

    def __init__(self):
        super().__init__()
        img_route = os.path.join(
            'glumtar', 'resources', 'images', 'ship0_0.png')
        self.image = pygame.image.load(img_route)
        self.image_n_width = self.image.get_width()/self.size_modifier
        self.image_n_height = self.image.get_height()/self.size_modifier

        self.img_new_size = pygame.transform.scale(
            self.image, (self.image_n_width, self.image_n_height))

        self.rect = self.img_new_size.get_rect(midleft=(self.margin, HEIGHT/2))

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0

        if pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
