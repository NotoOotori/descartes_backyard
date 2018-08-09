""" The class Keys"""
from key import Key


class Keys():
    """ Store the status of keys."""
    def __init__(self):
        self.k_up = Key()
        self.k_down = Key()
        self.k_left = Key()
        self.k_right = Key()
