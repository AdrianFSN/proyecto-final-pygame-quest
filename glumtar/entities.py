import os
import pygame
from . import HEIGHT, WIDTH


class Ship(pygame.sprite.Sprite):
    margin = 70
    speed = 5
    size_modifier = 4
    speed_boost = .7

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
