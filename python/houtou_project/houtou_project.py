""" The main file of 'Houtou Project'"""
import os

import pygame

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
    keys = Keys()

    # Create the player
    player = Player(settings, screen)

    # Start the main loop.
    while True:
        gf.check_events(player, keys)
        player.update()
        gf.update_screen(settings, screen, player)

# Run the game.
run_game()
