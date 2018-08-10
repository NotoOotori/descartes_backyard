""" The main file of 'Houtou Project'"""
import os

import pygame
from pygame.sprite import Sprite

import game_functions as gf
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
    pygame.display.set_caption("Houtou Project")
    screen_sprite = Sprite()
    screen_sprite.rect = screen.get_rect()
    keys = Keys()

    # Create the player with her bullet group
    player = Player(screen, settings)

    # Start the main loop.
    while True:
        gf.check_events(player, keys)
        player.update()
        gf.update_bullets(screen_sprite, player.bullets)
        gf.update_screen(screen, settings, player, player.bullets)

# Run the game.
run_game()
