""" The class Key"""
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
