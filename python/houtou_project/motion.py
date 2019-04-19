""" Class Motion """
from math import cos, radians, sin

class Motion():
    """ The base class to specify the motion of a Sprite. """
    def __init__(self, **kwargs):
        """ Initialize the motion.

        Keyword arguments:
        speed -- initial speed
        degree -- initial degree, rotating from ->, counterclockwise
        """
        super().__init__()
        self.speed = kwargs['speed']
        self.degree = kwargs['degree']

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            pass
        if name == 'speedx':
            return self.speed * cos(radians(self.degree))
        if name == 'speedy':
            return self.speed * sin(radians(self.degree))
        raise AttributeError('Attribute {} not found.'.format(name))

    def update_speed(self, **kwargs):
        """ Update the speed of the Sprite. """
        raise NotImplementedError(
            'Subclass must define update_speed method.')

class UniformlyAcceleratedLinearMotion(Motion):
    """ The linear motion of a Sprite. """
    def __init__(self, **kwargs):
        """ Initialize a new linear motion.

        Keyword arguments:
        speed -- initial speed
        acceleration --
        degree -- initial degree, rotating from ->, counterclockwise
        """
        super().__init__(**kwargs)
        self.acceleration = kwargs['acceleration']

    def update_speed(self, **kwargs):
        """ Update the speed of the Sprite. """
        self.speed += self.acceleration
