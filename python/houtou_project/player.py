"""The class Player"""
import pygame
from pygame.sprite import Group

from bullet import Bullet
from bullet_settings import BulletSettings
from circle import Circle


class Player():
    """ The class player"""
    def __init__(self, screen, settings):
        """ Initialize the player and set her initial position."""
        # Load the screen.
        self.screen = screen

        # Load the player's image and Rect object.
        self.image = pygame.image.load(settings.player_image_path)
        self.image = self.image.convert_alpha()
        self.alpha = 237
        self.image.fill((255, 255, 255, self.alpha), None,
                        pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect_origin = self.rect.copy()
        self.screen_rect = self.screen.get_rect()

        # Start the player at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store the float value of player's center.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Load the collision box.
        self.collision_box = Circle(settings.collision_box_color_edge,
                                    settings.collision_box_color_inside,
                                    settings.collision_box_radius,
                                    settings.collision_box_width)

        # Set the player's moving flags.
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Set the player's speed.
        self.speed = settings.player_speed

        # Create the bullet group of the player.
        bullet_filename = 'images/bullet1.png'
        bullet_alpha = 63
        bullet_speed = 10
        bullet_acceleration = 0.5
        self.bullet_degree = 270
        self.bullet_settings = BulletSettings(bullet_filename, bullet_alpha,
                                              bullet_speed, bullet_acceleration)
        self.bullets = Group()

        # Set the player's shooting flag
        self.shooting = False

    def update(self):
        """ Update the player's position, based on movement flags.
            Update the position of the collision box.
            Create new bullets, when the player is shooting."""
        # Update the float value of 'center'
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

        # Update the position of the collision box
        self.collision_box.update(self.rect.center)

        # Create new bullets at the center of the player.
        if self.shooting:
            new_bullet = Bullet(self.screen, self.bullet_settings,
                                self.bullet_degree)
            new_bullet.rect.center = self.rect.center
            new_bullet.centerx = float(new_bullet.rect.centerx)
            new_bullet.centery = float(new_bullet.rect.centery)
            self.bullets.add(new_bullet)

    def blitme(self):
        """ Draw the player without her collision box at their current
            location."""
        self.screen.blit(self.image, self.rect)
