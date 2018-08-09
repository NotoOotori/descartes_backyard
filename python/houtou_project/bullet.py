""" The class Bullet"""
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ A bullet."""
    def __init__(self, screen, bullet_settings, degree):
        """ Create a bullet at specified location."""
        super().__init__()
        self.screen = screen

        # Initialize the properties of the bullet.
        self.image = pygame.image.load(bullet_settings.filename).convert_alpha()
        self.alpha = bullet_settings.alpha
        self.image.fill((255, 255, 255, self.alpha), None,
                        pygame.BLEND_RGBA_MULT)
        self.image_origin = self.image.copy()
        self.rect = self.image.get_rect()
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.degree, self.speed, self.speedx, self.speedy = (None, None, None,
                                                             None)
        self.set_speed(bullet_settings.speed, degree)

    def set_speed(self, speed, degree):
        """ Update bullet's absolute speed and the projection on axises.
            Also rotate the image if needed."""
        self.speed = speed
        self.degree = degree
        self.speedx = self.speed * cos(radians(self.degree))
        self.speedy = self.speed * sin(radians(self.degree))
        self.image = self.image_origin
        pygame.transform.rotate(self.image, degree)

    def update(self): # pylint: disable=W0221
        """ Update the bullet's position."""
        self.centerx += self.speedx
        self.centery += self.speedy
        self.rect.center = self.centerx, self.centery

    def blitme(self):
        """ Draw the bullet at its current location."""
        self.screen.blit(self.image, self.rect)
