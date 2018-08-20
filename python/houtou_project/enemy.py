""" The class Enemy
    Note: Derived classes should override the Enemy.check_ticks()."""
import pygame
from pygame.sprite import Group, collide_mask


class Enemy():
    """ The class Enemy"""
    def __init__(self, screen, image_path, center, hit_point):
        """ Initialize the enemy and set her position."""
        self.screen = screen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.centerx, self.centery = float(center[0]), float(center[1])
        self.set_center(center)
        self.mask = pygame.mask.from_surface(self.image, 1)
        self.max_hp = hit_point
        self.hit_point = hit_point
        self.bullets = Group()

        # Store the frames passed after the enemy is created.
        self.ticks = 0

    def update(self, player)->bool:
        """ Update the enemy's health point."""
        for bullet in player.bullets.copy():
            if collide_mask(self, bullet):
                self.hit_point -= player.power
                player.bullets.remove(bullet)
        return self.hit_point <= 0

    def set_center(self, center):
        """ Set the center of the enemy."""
        self.centerx, self.centery = center
        self.rect.center = center

    def check_ticks(self):
        """ Post events based on the ticks."""
        self.ticks += 1

    def blitme(self):
        """ Draw the enemy to the screen."""
        self.screen.blit(self.image, self.rect)
