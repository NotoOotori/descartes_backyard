'''The class Circle'''
import pygame
import pygame.gfxdraw
from pygame.surface import Surface


class ShapeMeta(type):
    ''' The metaclass for Shape. '''
    def __call__(cls, *args, **kwargs):
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object

class Shape(metaclass=ShapeMeta):
    ''' The base class for shapes which can be drawn to a Surface. '''
    # pylint: disable=no-self-use

    image = None
    mask = None
    rect = None

    def check_required_attributes(self):
        ''' Raise error if required attributes are not implemented. '''
        if self.image is None:
            raise NotImplementedError(
                'Subclass must define self.image attribute.')
        if self.mask is None:
            raise NotImplementedError(
                'Subclass must define self.mask attribute.')
        if self.rect is None:
            raise NotImplementedError(
                'Subclass must define self.rect attribute.')

    def update(self, center: list):
        '''
        Update the position of the shape by giving coordinate of the center.
        '''
        raise NotImplementedError(
            "Subclass must define update method.")

    def blitme(self, surface: Surface):
        ''' Draw the shape to a Surface.'''
        raise NotImplementedError(
            "Subclass must define blitme method.")

class Circle(Shape):
    ''' A Circle which can be drawn to a Surface.'''
    def __init__(self, color_edge, color_inside, radius, width):
        ''' Initialize properties and the image of the circle.'''
        super().__init__()
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

    def update(self, center: list):
        '''
        Update the position of the circle by giving coordinate of the center.
        '''
        self.rect.center = center

    def blitme(self, surface: Surface):
        ''' Draw the circle to a Surface.'''
        surface.blit(self.image, self.rect)
