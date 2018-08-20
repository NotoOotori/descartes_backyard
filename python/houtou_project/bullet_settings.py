""" The class BulletSettings"""
class BulletSettings():
    """ Store the settings of a bullet."""
    def __init__(self, image, alpha, speed, acceleration=0):
        self.image = image
        self.alpha = alpha
        self.speed = speed
        self.acceleration = acceleration
