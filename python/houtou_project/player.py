"""The class Player"""
import pygame

from circle import Circle


class Player():
    """ The class player"""
    def __init__(self, settings, screen):
        """ Initialize the player and set her initial position."""
        # Load the screen.
        self.screen = screen
        self.settings = settings

        # Load the player's image, Rect object
        self.image = pygame.image.load(settings.player_image_path)
        self.image = self.image.convert_alpha()
        self.image.fill((255, 255, 255, 127), None, pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect_origin = self.rect.copy()
        self.screen_rect = self.screen.get_rect()

        # Start the player at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store the float value of player's center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Load the collision box
        self.collision_box = Circle(self.image,
                                    self.settings.collision_box_color_edge,
                                    self.settings.collision_box_color_inside,
                                    self.rect_origin,
                                    self.settings.collision_box_radius,
                                    self.settings.collision_box_width)

        # Draw the collision box to the player
        self.collision_box.blitme()

        # Set the player's moving flag
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Set the player's speed
        self.speed = settings.player_speed

    def update(self):
        """ Update the ship's position, based on movement flags."""
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.speed

        # Update the player's rect.
        self.rect.center = self.centerx, self.centery

    def blitme(self):
        """ Draw the player with her collision box at their current location."""
        self.screen.blit(self.image, self.rect)
