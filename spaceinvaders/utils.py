#!/usr/bin/python

import pygame
import os
from settings import (
    PLAYER_IMAGE, ENEMY_IMAGE, BULLET_IMAGE, BACKGROUND_IMAGE,
    HEART_IMAGE, SHOOT_SOUND, EXPLOSION_SOUND, BACKGROUND_MUSIC, SCREEN_WIDTH, SCREEN_HEIGHT
)

def load_image(path, width=None, height=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        return None

def load_sound(path):
    if not os.path.exists(path):
        print(f"Sound file not found: {path}")
        return None
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound at {path}: {e}")
        return None

def load_assets():
    assets = {}
    assets['player_img'] = load_image(PLAYER_IMAGE, 50, 38)
    assets['enemy_img'] = load_image(ENEMY_IMAGE, 50, 38)
    assets['bullet_img'] = load_image(BULLET_IMAGE, 10, 20)
    assets['background'] = load_image(BACKGROUND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT)
    assets['hearts_img'] = load_image(HEART_IMAGE, 20, 20) 

    assets['shoot_sound'] = load_sound(SHOOT_SOUND)
    assets['explosion_sound'] = load_sound(EXPLOSION_SOUND)

    if os.path.exists(BACKGROUND_MUSIC):
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            assets['background_music'] = BACKGROUND_MUSIC
        except pygame.error as e:
            print(f"Unable to load background music at {BACKGROUND_MUSIC}: {e}")
            assets['background_music'] = None
    else:
        print(f"Background music file not found: {BACKGROUND_MUSIC}")
        assets['background_music'] = None

    return assets
