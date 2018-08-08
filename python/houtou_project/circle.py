"""The class Circle"""
import pygame
import pygame.gfxdraw


class Circle():
    """ A Circle which can be drawn to a Surface"""
    def __init__(self, surface, color, size, radius):
        """ Initialize properties of the circle"""
        self.surface = surface
        self.color = color
        self.pos = (int(size.width/2), int(size.height/2))
        self.radius = radius

    def blitme(self):
        """ Draw the circle to a Surface."""
        pygame.gfxdraw.aacircle(self.surface, self.pos[0], self.pos[1],
                                self.radius, self.color)
        pygame.gfxdraw.filled_circle(self.surface, self.pos[0], self.pos[1],
                                     self.radius, self.color)
