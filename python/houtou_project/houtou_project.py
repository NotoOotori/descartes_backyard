""" The main file of Houtou Project"""
import os

import pygame
from pygame.sprite import Sprite
from pygame.time import Clock

import game_functions as gf
from enemies.enemy_repository import EnemyRepo
from keys import Keys
from player import Player
from settings import Settings


def run_game():
    """ The main function"""
    # Initialize the game and create a screen object.
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Houtou Project')
    screen_sprite = Sprite()
    screen_sprite.rect = screen.get_rect()
    keys = Keys()

    # Create the player with her bullet group.
    player = Player(screen)
    # Create the list of enemies.
    enemies = []
    # Load the enemies.
    enemy_repo = EnemyRepo(screen)

    bullets_list = []

    # Initialize the clock.
    clock = Clock()
    ticks = 0

    # Start the main loop.
    while True:
        gf.check_events(player, keys)
        gf.check_ticks(ticks, enemies, enemy_repo)
        # Update the player and the enemies.
        player.update()
        for enemy in enemies.copy():
            if enemy.update(player):
                enemies.remove(enemy)
            enemy.check_ticks(player)
        # Update the bullets.
        bullets_list = gf.get_bullets_list(player, enemies)
        gf.update_bullets(screen_sprite, bullets_list)
        # Update the screen.
        gf.update_screen(screen, settings, player, enemies, bullets_list)
        clock.tick(settings.fps)
        ticks += 1

# Run the game.
if __name__ == '__main__':
    run_game()
