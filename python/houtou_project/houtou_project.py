"""The main file of 'Houtou Project'"""
import os
import sys

import pygame

from settings import Settings


def run_game():
    """main function"""
    # Initialize the game and create a screen object.
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Houtou Project")

    # Start the main loop.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # 每次循环时都重绘屏幕
        screen.fill(ai_settings.bg_color)

        # 让最近绘制的屏幕可见
        pygame.display.flip()

        # 控制每秒的帧数
        pygame.time.Clock().tick(ai_settings.fps)

# Run the game.
run_game()
