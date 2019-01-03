""" Insertion Sort."""
import unittest


def insertion_sort(sequence):
    """ Return a new list containing all numbers
            from the sequence in ascending order."""
    A = sequence.copy() # pylint: disable=C0103
    for j, key in enumerate(A):
        i = j - 1
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
    return A

class InsertionSortTestCase(unittest.TestCase):
    """ Test the function insertion_sort."""
    def test_descending_sequence(self):
        """ [6, 5, 4, 3, 2, 1]."""
        sorted_sequence = insertion_sort([6, 5, 4, 3, 2, 1])
        self.assertEqual(sorted_sequence, [1, 2, 3, 4, 5, 6])

if __name__ == '__main__':
    unittest.main()
