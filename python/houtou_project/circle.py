"""The class Circle"""
import pygame
import pygame.gfxdraw


class Circle():
    """ A Circle which can be drawn to a Surface"""
    def __init__(self, surface, color_edge, color_inside, rect, radius, width):
        """ Initialize properties of the circle"""
        self.surface = surface
        self.color_edge = color_edge
        self.color_inside = color_inside
        self.pos = rect.center
        self.radius = radius
        self.width = width

    def blitme(self):
        """ Draw the circle to a Surface."""
        pygame.gfxdraw.aacircle(self.surface, self.pos[0], self.pos[1],
                                self.radius, self.color_edge)
        pygame.gfxdraw.filled_circle(self.surface, self.pos[0], self.pos[1],
                                     self.radius, self.color_edge)
        pygame.gfxdraw.aacircle(self.surface, self.pos[0], self.pos[1],
                                self.radius - self.width, self.color_inside)
        pygame.gfxdraw.filled_circle(self.surface, self.pos[0], self.pos[1],
                                     self.radius - self.width,
                                     self.color_inside)
