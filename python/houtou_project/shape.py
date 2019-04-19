"""The class Circle"""
import pygame
import pygame.image
import pygame.gfxdraw
import pygame.mask
from pygame.sprite import Sprite
from pygame.surface import Surface


class Shape(Sprite):
    """ The base class for shapes which can be drawn to a Surface. """
    def __init__(self, **kwargs):
        super().__init__()
        self.screen = kwargs['screen']
        self.image = self._get_image(**kwargs)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 1)

    def _get_image(self, **kwargs) -> Surface:
        """
        Get the image of the shape.
        """
        raise NotImplementedError(
            'Subclass must define _get_image method.')

    def update(self, *args):
        """
        Update the position of the shape by giving coordinate of the center.
        """
        self.rect.center = args[0]

    def blitme(self):
        """ Draw the shape to a Surface."""
        self.screen.blit(self.image, self.rect)

class CircleShape(Shape):
    """ A Circle which can be drawn to a Surface. """
    def __init__(self, **kwargs):
        """ Initialize properties and the image of the circle.

        Keyword arguments:
        alpha --
        color_edge --
        color_inside --
        radius -- radius of the whole circle
        width -- width of the edge
        screen -- (inherited)
        """
        # pylint: disable=useless-super-delegation
        super().__init__(**kwargs)

    def _get_image(self, **kwargs) -> Surface:
        # Parse keyword arguments.
        alpha = kwargs['alpha']
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
        image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        return image

class ImageShape(Shape):
    """ A Image which can be drawn to a Surface. """
    def __init__(self, **kwargs):
        """ Initialize properties and the image of the circle.

        Keyword arguments:
        image --
        screen -- (inherited)
        """
        # pylint: disable=useless-super-delegation
        super().__init__(**kwargs)

    def _get_image(self, **kwargs) -> Surface:
        return kwargs['image']
