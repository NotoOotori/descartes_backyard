""" The main file of 'Houtou Project'"""
import os
import sys

import pygame

from player import Player
from settings import Settings


def run_game():
    """ The main function"""
    # Initialize the game and create a screen object.
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Houtou Project")

    # Create the player
    player = Player(ai_settings, screen)

    # Start the main loop.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Redraw the screen, each pass through the loop.
        screen.fill(ai_settings.bg_color)
        player.blitme()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

        # Control the frames per second
        pygame.time.Clock().tick(ai_settings.fps)

# Run the game.
run_game()
