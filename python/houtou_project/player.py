"""The class Player"""
import pygame

from circle import Circle


class Player():
    """ The class player"""
    def __init__(self, ai_settings, screen):
        """ Initialize the player and set her initial position."""
        # Load the screen.
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the player's image, Rect object
        self.image = pygame.image.load(ai_settings.player_image_path)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start the player at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Load the player's collision box
        self.collision_box = Circle(self.image, (255, 255, 0), self.rect, 6)

    def blitme(self):
        """ Draw the player and her collision box at their current location."""
        self.collision_box.blitme()
        self.screen.blit(self.image, self.rect)
