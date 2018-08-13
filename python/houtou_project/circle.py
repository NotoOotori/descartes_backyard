"""The class Circle"""
import pygame
import pygame.gfxdraw
from pygame.surface import Surface


class Circle():
    """ A Circle which can be drawn to a Surface."""
    def __init__(self, color_edge, color_inside, radius, width):
        """ Initialize properties and the image of the circle."""
        self.image = Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.color_edge = color_edge
        self.color_inside = color_inside
        self.radius = radius
        self.width = width

        # Initialize the image.
        pygame.gfxdraw.aacircle(self.image, self.radius, self.radius,
                                self.radius, self.color_edge)
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius,
                                     self.radius, self.color_edge)
        pygame.gfxdraw.aacircle(self.image, self.radius, self.radius,
                                self.radius - self.width, self.color_inside)
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius,
                                     self.radius - self.width,
                                     self.color_inside)

        # Initialize the mask.
        self.mask = pygame.mask.from_surface(self.image, 1)

    def update(self, center):
        """ Update the position of the circle."""
        self.rect.center = center

    def blitme(self, surface):
        """ Draw the circle to a Surface."""
        surface.blit(self.image, self.rect)
