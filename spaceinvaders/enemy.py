#!/usr/bin/python

import pygame
import random
from settings import ENEMY_SPEED, BULLET_SPEED, BULLET_COOLDOWN, SCREEN_WIDTH
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, assets, all_sprites, bullets_group):
        super().__init__()
        self.image = assets['enemy_img']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.direction = 1 
        self.assets = assets
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group
        self.last_shot = pygame.time.get_ticks()
        self.shoot_cooldown = BULLET_COOLDOWN

    def update(self, *args, **kwargs):
        self.rect.x += self.speed * self.direction

        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 30

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_cooldown:
            if random.random() < 0.01: 
                self.shoot()
                self.last_shot = now

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, BULLET_SPEED, self.assets['bullet_img'], direction='down')
        self.all_sprites.add(bullet)
        self.bullets_group.add(bullet)
        if self.assets['shoot_sound']:
            self.assets['shoot_sound'].play()
