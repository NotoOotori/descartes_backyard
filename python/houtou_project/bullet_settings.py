""" The class BulletSettings"""
import pygame


class BulletSettings():
    """ Store the settings of a bullet."""
    def __init__(self, filename, alpha, speed, acceleration):
        self.image = pygame.image.load(filename).convert_alpha()
        self.alpha = alpha
        self.speed = speed
        self.acceleration = acceleration
