''' Functions for the project.'''
from numpy import sign

from constants import Constant


def _first_two_char(chess_state, move):
    move_chs = ''
    flag = False
    player = chess_state['player']
    names = move[:2], move[-2:]
    piece = chess_state[names[0]]
    piece_chs = Constant.piece[player + piece.lower()]
    ver_lines = (get_vertical_line(names[0], player),
                 get_vertical_line(names[1], player))
    for yname in '123456789':
        name = names[0][0] + yname
        if chess_state[name] == piece:
            if calc_delta(names[0] + name)[1] < 0:
                move_chs += '前{}'.format(piece_chs)
                flag = True
            elif calc_delta(names[0] + name)[1] > 0:
                move_chs += '后{}'.format(piece_chs)
                flag = True
    if not flag:
        move_chs += '{}{}'.format(piece_chs, ver_lines[0])
    return move_chs

def calc_delta(move, player=None):
    ''' Return the delta of the piece according to the player.'''
    names = move[:2], move[-2:]
    delta_1 = letter_to_number(names[1][0]) - letter_to_number(names[0][0])
    delta_2 = int(names[1][1]) - int(names[0][1])
    if player is None:
        return (delta_1, delta_2)
    if player == 'b':
        return (delta_1, -delta_2)
    return (-delta_1, delta_2)

def count_piece(chess_state, move):
    ''' Return the number of pieces the straight move will go through.'''
    delta = calc_delta(move)
    count = 0
    if delta[0] == 0:
        for ydelta in range(sign(delta[1]), delta[1], sign(delta[1])):
            if chess_state[name_addition(move, (0, ydelta))] is not None:
                count += 1
        return count
    if delta[1] == 0:
        for xdelta in range(sign(delta[0]), delta[0], sign(delta[0])):
            if chess_state[name_addition(move, (xdelta, 0))] is not None:
                count += 1
        return count
    raise Exception('Not a straight move!')

def dbc_to_sbc(char):
    ''' Convert a one-character string in DBC case to the one in SBC case.'''
    code = ord(char)
    if code == 32:
        return chr(12288)
    if code >= 33 and code <= 126:
        return chr(code + 65248)
    raise Exception('Not a DBC-case-character!')

def flip_player(player):
    ''' Return the player other than the one recieved.'''
    if player == 'b':
        return 'w'
    return 'b'

def format_number(number, player, flag=None):
    ''' Format the number.'''
    if flag == 'vert':
        if player == 'b':
            return dbc_to_sbc(str(number))
        return '九八七六五四三二一'[number - 1]
    if player == 'b':
        return dbc_to_sbc(str(number))
    return '一二三四五六七八九'[number - 1]

def format_round(round_num, player):
    ''' Format the round to display at listbox.'''
    round_str = str(round_num)
    length = len(round_str)
    if player == 'b':
        return ' ' * 5
    if length >= 3:
        return '{}.{}'.format(round_str[-3:], ' ')
    return '{}{}.{}'.format(' ' * (3 - length), round_num, ' ')

def get_bishop_eye(move):
    ''' Return the bishop's eye according to the move.'''
    delta = calc_delta(move)
    name_origin = move[:2]
    if delta == (-2, -2):
        return name_addition(name_origin, (-1, -1))
    if delta == (-2, 2):
        return name_addition(name_origin, (-1, 1))
    if delta == (2, -2):
        return name_addition(name_origin, (1, -1))
    if delta == (2, 2):
        return name_addition(name_origin, (1, 1))
    raise Exception("Not a bishop's move!")

def get_knight_leg(move):
    ''' Return the knight's leg according to the move.'''
    delta = calc_delta(move)
    name_origin = move[:2]
    if delta[0] == -2:
        return name_addition(name_origin, (-1, 0))
    if delta[0] == 2:
        return name_addition(name_origin, (1, 0))
    if delta[1] == -2:
        return name_addition(name_origin, (0, -1))
    if delta[1] == 2:
        return name_addition(name_origin, (0, 1))
    raise Exception("Not a knight's move!")

def get_vertical_line(name, player):
    ''' Return the vertical line of the grid.'''
    number = letter_to_number(name[0])
    return format_number(number, player, 'vert')

def letter_to_number(letter):
    ''' Convert a letter to a number.'''
    return ord(letter) - 96

def name_addition(name, delta):
    ''' Return the new name after a move of delta.'''
    new_xname = number_to_letter(letter_to_number(name[0]) + delta[0])
    new_yname = str(int(name[1]) + delta[1])
    new_name = new_xname + new_yname
    return new_name

def number_to_letter(number):
    ''' Convert a number to a letter.'''
    return chr(number + 96)

def to_chinese_format(chess_state, move):
    ''' Return the chinese vertical format of a move.'''
    move_chs = ''
    player = chess_state['player']
    delta = calc_delta(move, player)
    names = move[:2], move[-2:]
    piece = chess_state[names[0]]
    piece_chs = Constant.piece[player + piece.lower()]
    ver_lines = (get_vertical_line(names[0], player),
                 get_vertical_line(names[1], player))
    if piece.lower() in 'ab':
        if delta[1] > 0:
            move_chs = '{}{}进{}'.format(piece_chs, ver_lines[0], ver_lines[1])
        elif delta[1] < 0:
            move_chs = '{}{}退{}'.format(piece_chs, ver_lines[0], ver_lines[1])
    elif piece.lower() in 'ckr':
        move_chs += _first_two_char(chess_state, move)
        if delta[1] == 0:
            move_chs += '平{}'.format(ver_lines[1])
        elif delta[1] > 0:
            move_chs += '进{}'.format(format_number(delta[1], player))
        elif delta[1] < 0:
            move_chs += '退{}'.format(format_number(-delta[1], player))
    elif piece.lower() == 'n':
        move_chs += _first_two_char(chess_state, move)
        if delta[1] > 0:
            move_chs += '进{}'.format(ver_lines[1])
        elif delta[1] < 0:
            move_chs += '退{}'.format(ver_lines[1])
    elif piece.lower() == 'p':
        move_chs += _first_two_char(chess_state, move)
        if delta[1] == 0:
            move_chs += '平{}'.format(ver_lines[1])
        elif delta[1] > 0:
            move_chs += '进{}'.format(format_number(delta[1], player))
        elif delta[1] < 0:
            move_chs += '退{}'.format(format_number(-delta[1], player))
    return move_chs
