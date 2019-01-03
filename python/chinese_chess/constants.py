''' Store some constants.'''
from itertools import chain, product


class ValidDelta(dict):
    ''' Store all valid deltas for each piece.'''
    def __init__(self):
        super().__init__()
        self['a'] = tuple(product([-1, 1], repeat=2))
        self['b'] = tuple(product([-2, 2], repeat=2))
        self['c'] = tuple(chain(((x, 0) for x in range(-8, 9) if x != 0),
                                ((0, y) for y in range(-9, 10) if y != 0)))
        self['k'] = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self['n'] = ((-2, -1), (-1, -2), (-2, 1), (-1, 2),
                     (2, -1), (1, -2), (2, 1), (1, 2))
        self['p'] = ((-1, 0), (1, 0), (0, 1))
        self['r'] = self['c']

class Constant():
    ''' Store some constants.'''
    initial_fen = 'rnbakabnr/9/1c5c1/p1p1p1p1p/' + \
                  '9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'
    iter_chessboard_id_name = list(
        product(enumerate('abcdefghi'), enumerate('9876543210')))
    valid_delta = ValidDelta()
    piece = {'wa': '仕', 'wb': '相', 'wc': '炮', 'wk': '帅',
             'wn': '马', 'wp': '兵', 'wr': '车',
             'ba': '士', 'bb': '象', 'bc': '炮', 'bk': '将',
             'bn': '马', 'bp': '卒', 'br': '车'}
