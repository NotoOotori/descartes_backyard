"""The class Circle"""
import pygame
import pygame.gfxdraw
import pygame.mask
from pygame.surface import Surface


class Shape():
    """ The base class for shapes which can be drawn to a Surface. """

    def __init__(self, **kwargs):
        self.image = self._get_image(**kwargs)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 1)

    def _get_image(self, **kwargs) -> Surface:
        """
        Get the image of the shape.
        """
        raise NotImplementedError(
            "Subclass must define get_image method.")

    def update(self, center: list):
        """
        Update the position of the shape by giving coordinate of the center.
        """
        self.rect.center = center

    def blitme(self, surface: Surface):
        """ Draw the shape to a Surface."""
        surface.blit(self.image, self.rect)

class Circle(Shape):
    """ A Circle which can be drawn to a Surface."""
    def __init__(self, **kwargs):
        """ Initialize properties and the image of the circle.

        Keyword arguments:
        color_edge --
        color_inside --
        radius -- radius of the whole circle
        width -- width of the edge
        """
        # pylint: disable=useless-super-delegation
        super().__init__(**kwargs)

    def _get_image(self, **kwargs) -> Surface:
        # Parse keyword arguments.
        color_edge = kwargs['color_edge']
        color_inside = kwargs['color_inside']
        radius = kwargs['radius']
        width = kwargs['width']

        # Create the image.
        image = Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(image, radius, radius, radius, color_edge)
        pygame.gfxdraw.filled_circle(image, radius, radius, radius, color_edge)
        pygame.gfxdraw.aacircle(
            image, radius, radius, radius - width, color_inside)
        pygame.gfxdraw.filled_circle(
            image, radius, radius, radius - width, color_inside)
        return image
