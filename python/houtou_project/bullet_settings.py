""" The class BulletSettings"""
# TODO: Restruct bullet_settings.
"""
Maybe first create a base class,
and then add subclasses like CircleBulletSettings.
"""
class BulletSettings():
    """ Store the settings of a bullet."""
    def __init__(self, image, alpha, speed, acceleration=0):
        self.image = image
        self.alpha = alpha
        self.speed = speed
        self.acceleration = acceleration
