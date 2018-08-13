"""The class Circle"""
import pygame
import pygame.gfxdraw


class Circle():
    """ A Circle which can be drawn to a Surface"""
    def __init__(self, color_edge, color_inside, radius, width):
        """ Initialize properties of the circle"""
        self.color_edge = color_edge
        self.color_inside = color_inside
        self.radius = radius
        self.width = width

    def blitme(self, surface, center):
        """ Draw the circle to a Surface."""
        pygame.gfxdraw.aacircle(surface, center[0], center[1], self.radius,
                                self.color_edge)
        pygame.gfxdraw.filled_circle(surface, center[0], center[1],
                                     self.radius, self.color_edge)
        pygame.gfxdraw.aacircle(surface, center[0], center[1],
                                self.radius - self.width, self.color_inside)
        pygame.gfxdraw.filled_circle(surface, center[0], center[1],
                                     self.radius - self.width,
                                     self.color_inside)
