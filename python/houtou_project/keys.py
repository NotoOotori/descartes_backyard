""" The classes Key and Keys"""
class Key():
    """ Store the status of a key."""
    def __init__(self):
        self.hold = False

    def press(self):
        """ Record the key press."""
        self.hold = True

    def release(self):
        """ Record the key release."""
        self.hold = False

class Keys():
    """ Store the status of keys."""
    def __init__(self):
        self.k_up = Key()
        self.k_down = Key()
        self.k_left = Key()
        self.k_right = Key()
        self.k_z = Key()
