#!/usr/bin/python
import pygame

def check_collision(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)
