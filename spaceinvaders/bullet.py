#!/usr/bin/python

import pygame
from settings import BULLET_SPEED, SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image, direction='up'):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if direction == 'up':
            self.rect.bottom = y
            self.speed = -speed
        elif direction == 'down':
            self.rect.top = y
            self.speed = speed
        self.direction = direction

    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        # removes bullet when offscreen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
