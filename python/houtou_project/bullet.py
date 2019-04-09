''' Store all classes related to bullet.'''
from math import atan2, cos, degrees, radians, sin

import pygame
from pygame.sprite import Group, Sprite


class Bullet(Sprite):
    ''' A bullet.'''
    def __init__(self, screen, bullet_settings, center, degree):
        ''' Create a bullet at specified location.'''
        super().__init__()
        self.screen = screen

        # Initialize the properties of the bullet.
        self.image = bullet_settings.image.copy()
        self.alpha = bullet_settings.alpha
        self.image.fill((255, 255, 255, self.alpha), None,
                        pygame.BLEND_RGBA_MULT)
        self.image_origin = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Initialize the mask.
        self.mask = pygame.mask.from_surface(self.image, 1)
        # Initialize speed related contents.
        self.degree, self.speed, self.speedx, self.speedy = (None, None, None,
                                                             None)
        self.acceleration = bullet_settings.acceleration
        self.set_speed(bullet_settings.speed, degree, 0)

    def set_speed(self, speed, degree, acceleration=0):
        ''' Update bullet's absolute speed and the projection on axises.
            Also rotate the image if needed.'''
        self.speed = speed + acceleration
        self.degree = degree
        self.speedx = self.speed * cos(radians(self.degree))
        self.speedy = self.speed * sin(radians(self.degree))
        self.image = self.image_origin
        self.image = pygame.transform.rotate(self.image, 270 - degree)

    def update(self): # pylint: disable=W0221
        ''' Update the bullet's position and accelerate the bullet.'''
        self.centerx += self.speedx
        self.centery += self.speedy
        self.rect.center = self.centerx, self.centery
        self.set_speed(self.speed, self.degree, self.acceleration)

    def blitme(self):
        ''' Draw the bullet at its current location.'''
        self.screen.blit(self.image, self.rect)

class GeneralSniperBullet(Group):
    ''' A group that contains one row of the general sniper bullets.'''
    def __init__(self, screen, bullet_settings, enemy, player, way,
                 degree_width):
        super().__init__()
        degree = degrees(atan2(player.rect.y - enemy.rect.y,
                               player.rect.x - enemy.rect.x))
        for i in range(way):
            # If they are even-way sniper bullets.
            if way % 2 == 0:
                if i % 2 == 0:
                    new_degree = degree + degree_width*(i + 1)/2
                elif i % 2 == 1:
                    new_degree = degree - degree_width*i/2
            # If they are odd-way sniper bullets.
            elif way % 2 == 1:
                if i % 2 == 0:
                    new_degree = degree + degree_width*i/2
                elif i % 2 == 1:
                    new_degree = degree - degree_width*(i + 1)/2
            new_bullet = Bullet(screen, bullet_settings,
                                enemy.rect.center, new_degree)
            self.add(new_bullet)
