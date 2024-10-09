#!/usr/bin/python

import pygame
from settings import PLAYER_SPEED, PLAYER_COOLDOWN, BULLET_SPEED, BULLET_COOLDOWN, SCREEN_WIDTH
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, assets, all_sprites, bullets_group):
        super().__init__()
        self.image = assets['player_img']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = PLAYER_SPEED
        self.last_shot = pygame.time.get_ticks()
        self.shoot_cooldown = PLAYER_COOLDOWN
        self.assets = assets
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group
        
        self.max_health = 8  # 8 hearts (lives)
        self.current_health = self.max_health

    def update(self, keys_pressed, *args, **kwargs):
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top, BULLET_SPEED, self.assets['bullet_img'])
            self.all_sprites.add(bullet)
            self.bullets_group.add(bullet)
            if self.assets['shoot_sound']:
                self.assets['shoot_sound'].play()
            self.last_shot = now

    def take_damage(self, damage=1):
        """Decrease the player's health."""
        self.current_health -= damage
        print(f"Player Health: {self.current_health}/{self.max_health}")
        if self.current_health <= 0:
            self.kill()
