""" Linear Search."""
def linear_search(sequence, key):
    """ Return the first index of key in the sequence
            or the special value None if key does not appear in the sequence"""
    for i, value in enumerate(sequence):
        if value == key:
            return i
    return None
