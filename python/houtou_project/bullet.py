""" Store all classes related to bullet."""
from math import atan2, degrees

import pygame
from pygame.sprite import Group, Sprite

from motion import UniformlyAcceleratedLinearMotion
from shape import CircleShape


class Bullet(Sprite):
    """ A circle bullet which moves linearly. """
    def __init__(self, center, **kwargs):
        """ Create a bullet at specified location.

        Keyword arguments:
        shape_type -- the class name of the shape
        arguments for shape_type.__init__
        motion_type -- the class name of the motion
        arguments for motion_type.__init__
        """
        super().__init__()

        shape_type = globals()[kwargs["shape_type"]]
        motion_type = globals()[kwargs["motion_type"]]

        self.shape = shape_type(**kwargs)
        self.motion = motion_type(**kwargs)

        # Initialize the properties of the bullet.
        self.image_origin = self.image.copy()
        self.rect.center = center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def __getattr__(self, name):
        for child in (self.shape, self.motion):
            try:
                return getattr(child, name)
            except AttributeError:
                pass
        raise AttributeError('Attribute {} not found.'.format(name))

    def update(self, *args):
        """ Update the bullet's position, speed and image. """
        self.centerx += self.speedx
        self.centery += self.speedy
        self.rect.center = self.centerx, self.centery
        self.update_speed()
        self.image = pygame.transform.rotate(
            self.image_origin, 270 - self.degree)

    def blitme(self):
        """ Draw the bullet at its current location."""
        self.screen.blit(self.image, self.rect)

# class GeneralSniperBullet(Group):
#     """ A group that contains one row of the general sniper bullets."""
#     # TODO: Refactor __init__.
#     def __init__(self, screen, bullet_settings, enemy, player, way,
#                  degree_width):
#         super().__init__()
#         degree = degrees(atan2(player.rect.y - enemy.rect.y,
#                                player.rect.x - enemy.rect.x))
#         for i in range(way):
#             # If they are even-way sniper bullets.
#             if way % 2 == 0:
#                 if i % 2 == 0:
#                     new_degree = degree + degree_width*(i + 1)/2
#                 elif i % 2 == 1:
#                     new_degree = degree - degree_width*i/2
#             # If they are odd-way sniper bullets.
#             elif way % 2 == 1:
#                 if i % 2 == 0:
#                     new_degree = degree + degree_width*i/2
#                 elif i % 2 == 1:
#                     new_degree = degree - degree_width*(i + 1)/2
#             new_bullet = Bullet(screen, bullet_settings,
#                                 enemy.rect.center, new_degree)
#             self.add(new_bullet)
