#!/usr/bin/python

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, GREEN
from utils import load_assets
from player import Player
from enemy import Enemy
from collision import check_collision

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moon Invaders")
    clock = pygame.time.Clock()

    assets = load_assets()

    if assets['background_music']:
        pygame.mixer.music.play(-1)

    all_sprites = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, assets, all_sprites, bullets_group)
    all_sprites.add(player)

    for row in range(3):
        for i in range(10):
            enemy = Enemy(70 + i * 60, 50 + row * 50, assets, all_sprites, bullets_group)
            all_sprites.add(enemy)
            enemies_group.add(enemy)

    score = 0
    font = pygame.font.SysFont(None, 36)
    controls_font = pygame.font.SysFont(None, 24) 
    game_over = False

    controls_text = [
        "Spacebar: Shoot",
        "Left Arrow or A: Move Left",
        "Right Arrow or D: Move Right"
    ]

    controls_surface = pygame.Surface((250, 60), pygame.SRCALPHA)
    controls_surface.fill((0, 0, 0, 0))

    for idx, line in enumerate(controls_text):
        text_surface = controls_font.render(line, True, WHITE)
        text_surface.set_alpha(150) 
        controls_surface.blit(text_surface, (0, idx * 20))

    controls_rect = controls_surface.get_rect()
    controls_rect.bottomright = (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)

    running = True
    while running:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                else:
                    if event.key == pygame.K_RETURN:
                        main()  # restart game

        if not game_over:
            all_sprites.update(keys_pressed)

            for bullet in bullets_group:
                if bullet.direction == 'up':
                    hit_enemies = pygame.sprite.spritecollide(bullet, enemies_group, True)
                    for enemy in hit_enemies:
                        score += 1000
                        bullet.kill()
                        if assets['explosion_sound']:
                            assets['explosion_sound'].play()

            for bullet in bullets_group:
                if bullet.direction == 'down':
                    if check_collision(bullet, player):
                        player.take_damage()  # decrease health
                        bullet.kill()
                        if assets['explosion_sound']:
                            assets['explosion_sound'].play()
                        if player.current_health <= 0:
                            game_over = True
                            if assets['background_music']:
                                pygame.mixer.music.stop()

            for enemy in enemies_group:
                if enemy.rect.bottom >= player.rect.top:
                    game_over = True
                    if assets['background_music']:
                        pygame.mixer.music.stop()

            if not enemies_group:
                game_over = True

        if assets['background']:
            screen.blit(assets['background'], (0, 0))
        else:
            screen.fill(BLACK)

        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            if enemies_group:
                message = "Game Over! Press 'Enter' to Restart"
            else:
                message = "You Win! Press 'Enter' to Restart"
            game_over_text = font.render(message, True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        sound_status = "Sound: ON" if assets['shoot_sound'] or assets['explosion_sound'] or assets['background_music'] else "Sound: OFF"
        sound_text = font.render(sound_status, True, WHITE)
        screen.blit(sound_text, (SCREEN_WIDTH - sound_text.get_width() - 10, 10))

        if player:
            hearts = player.current_health
            for i in range(hearts):
                heart_x = 10 + i * (assets['hearts_img'].get_width() + 5)
                heart_y = 50 
                screen.blit(assets['hearts_img'], (heart_x, heart_y))

        screen.blit(controls_surface, controls_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
