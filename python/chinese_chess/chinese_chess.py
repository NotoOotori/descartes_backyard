''' A simple chinese chess program.
    Syntax: chinese_chess.py [{-g | --gamestring} <gamestring>]
                             [{-s | --state} <state>]
'''
import getopt
import os
import re
import sys
import tkinter as tk
from copy import deepcopy
from itertools import product
from tkinter.messagebox import askyesnocancel  # pylint: disable=C0412

import functions as func
from constants import Constant


def main(argv):
    ''' Main function.'''
    help_str = 'chiness_chess [{-g | --gamestring} <gamestring>] [{-s | --state} <state>]'
    kwargs = {}
    try:
        opts, _ = getopt.getopt(argv, 'hg:s:', ['help', 'gamestring=', 'state='])
    except getopt.GetoptError:
        print(help)
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_str)
            sys.exit()
        elif opt in ('-g', '--gamestring'):
            kwargs['game_string'] = arg
        elif opt in ('-s', '--state'):
            kwargs['state'] = arg
    root = ChineseChess(**kwargs)
    root.mainloop()

class Chessboard(tk.Canvas):
    ''' The chess board.'''
    def __init__(self, root, images, **kwargs):
        super().__init__(master=root, width=456, height=512,
                         borderwidth=2, relief=tk.RIDGE)
        if 'state' in kwargs.keys():
            state = kwargs['state']
        else:
            state = 'normal'
        if 'game_string' in kwargs.keys():
            game_string = kwargs['game_string']
        else:
            game_string = Constant.initial_fen + ';'
        self.root = root
        self.images = images
        self.chess_state = None
        self.chess_states = None
        self.turn = 0
        moves = self._load(game_string)
        self._setup_widgets()
        if moves != ['']:
            for move in moves:
                self._move(move)
            self._reset_masks()
        self.last_name = None
        if state == 'normal':
            for (_, xname), (_, yname) in Constant.iter_chessboard_id_name:
                name = xname + yname
                self.tag_bind(
                    name, '<Button-1>',
                    lambda event, name=name: self._on_click(event, name))
        # self.bind('<Motion>', print)

    def _create_image_at_square(self, name, **kwargs):
        items = self.find_withtag(name)
        squares = self.find_withtag('square')
        square = [item for item in items if item in squares]
        coords = self.coords(square)
        return self.create_image(
            (coords[0] + coords[2])//2, (coords[1] + coords[3])//2, **kwargs)

    def _delete_mask(self, cur_player):
        masks = self.find_withtag('mask')
        player = func.flip_player(cur_player)
        items = self.find_withtag(player)
        for mask in masks:
            if mask in items:
                self.delete(mask)

    def _draw(self, grid_x, grid_y):
        grain = self.images['wood_grain']
        self.create_image(0, 0, image=grain, anchor=tk.NW)
        self._draw_board(grid_x, grid_y)

    def _draw_board(self, grid_x, grid_y):
        # Draw the grids.
        for x in range(9): # pylint: disable=C0103
            if x in (0, 8):
                self.create_line(grid_x[x], grid_y[0], grid_x[x], grid_y[-1]+1)
            else:
                self.create_line(grid_x[x], grid_y[0], grid_x[x], grid_y[4])
                self.create_line(grid_x[x], grid_y[-5], grid_x[x], grid_y[-1])
        for y in range(10): # pylint: disable=C0103
            self.create_line(grid_x[0], grid_y[y], grid_x[-1]+1, grid_y[y])

        # Draw the frame.
        self.create_line(grid_x[0]-6, grid_y[0]-8, grid_x[0]-6, grid_y[-1]+8,
                         width=4)
        self.create_line(grid_x[-1]+6, grid_y[0]-8, grid_x[-1]+6, grid_y[-1]+8,
                         width=4)
        self.create_line(grid_x[0]-8, grid_y[0]-6, grid_x[-1]+8, grid_y[0]-6,
                         width=4)
        self.create_line(grid_x[0]-8, grid_y[-1]+6, grid_x[-1]+8, grid_y[-1]+6,
                         width=4)

        # Draw 'X's.
        for y in (-1, 2): # pylint: disable=C0103
            self.create_line(grid_x[3], grid_y[y-2], grid_x[5], grid_y[y])
            self.create_line(grid_x[5], grid_y[y-2], grid_x[3], grid_y[y])

        # Draw '╬'s.
        self._draw_board_misc(grid_x, grid_y)

    def _draw_board_misc(self, grid_x, grid_y):
        length, gap, width = 10, 4, 2
        coordinates = list(product(range(0, 10, 2), [3, -4])) + \
                      list(product([1, -2], [2, -3]))
        for x, y in coordinates: # pylint: disable=C0103
            if x != 0:
                self.create_line(grid_x[x] - (length + gap), grid_y[y] - gap,
                                 grid_x[x] - gap, grid_y[y] - gap, width=width)
                self.create_line(grid_x[x] - gap, grid_y[y] - (length + gap),
                                 grid_x[x] - gap, grid_y[y] - gap, width=width)
                self.create_line(grid_x[x] - (length + gap), grid_y[y] + gap,
                                 grid_x[x] - gap, grid_y[y] + gap, width=width)
                self.create_line(grid_x[x] - gap, grid_y[y] + (length + gap),
                                 grid_x[x] - gap, grid_y[y] + gap, width=width)
            if x != 8:
                self.create_line(grid_x[x] + (length + gap), grid_y[y] - gap,
                                 grid_x[x] + gap, grid_y[y] - gap, width=width)
                self.create_line(grid_x[x] + gap, grid_y[y] - (length + gap),
                                 grid_x[x] + gap, grid_y[y] - gap, width=width)
                self.create_line(grid_x[x] + (length + gap), grid_y[y] + gap,
                                 grid_x[x] + gap, grid_y[y] + gap, width=width)
                self.create_line(grid_x[x] + gap, grid_y[y] + (length + gap),
                                 grid_x[x] + gap, grid_y[y] + gap, width=width)

    def _draw_mask(self, name, flag=None):
        player = self.chess_state['player']
        if flag == 'flip_player':
            player = func.flip_player(player)
        image = self.images['mm']
        tags = [name, 'mask', player]
        mask = self._create_image_at_square(name, image=image, tag=tags)
        self.tag_bind(mask, '<Button-1>',
                      lambda event, name=name: self._on_click(event, name))

    def _is_current_player(self, piece):
        if self.chess_state['player'] == 'b':
            return piece.islower()
        return piece.isupper()

    def _is_inside_castle(self, name):
        if self.chess_state['player'] == 'b':
            if name in map(''.join, product('def', '789')):
                return True
            return False
        if name in map(''.join, product('def', '012')):
            return True
        return False

    def _is_castle_side(self, name):
        if self.chess_state['player'] == 'b':
            if int(name[1]) in list(range(5, 10)):
                return True
            return False
        if int(name[1]) in list(range(0, 5)):
            return True
        return False

    def _is_valid_move(self, move):
        player = self.chess_state['player']
        names = move[:2], move[-2:]
        piece = self.chess_state[names[0]].lower()
        delta = func.calc_delta(move, player)
        if delta not in Constant.valid_delta[piece]:
            return False
        if piece == 'a':
            if self._is_inside_castle(names[1]):
                return True
            return False
        if piece == 'b':
            if self._is_castle_side(names[1]):
                if self.chess_state[func.get_bishop_eye(move)] is None:
                    return True
            return False
        if piece == 'c':
            if self.chess_state[names[1]] is None:
                if func.count_piece(self.chess_state, move) == 0:
                    return True
                return False
            if func.count_piece(self.chess_state, move) == 1:
                return True
            return False
        if piece == 'k':
            if self._is_inside_castle(names[1]):
                return True
            return False
        if piece == 'n':
            if self.chess_state[func.get_knight_leg(move)] is None:
                return True
            return False
        if piece == 'p':
            if not self._is_castle_side(names[1]):
                return True
            if delta == (0, 1):
                return True
            return False
        if piece == 'r':
            if func.count_piece(self.chess_state, move) == 0:
                return True
            return False
        raise Exception('What the hell piece it is!')

    def _load(self, game_string):
        fen, moves_str = game_string.split(';')
        moves = moves_str.split(' ')
        self.chess_state = ChessState(fen)
        self.chess_states = [deepcopy(self.chess_state)]
        return moves

    def _move(self, move):
        self.root.chess_manual.insert_move(self.chess_state, self.turn, move)
        names = move[:2], move[-2:]
        squares = self.find_withtag('square')
        pieces = self.find_withtag('piece')
        items_1 = self.find_withtag(names[0])
        items_2 = self.find_withtag(names[1])
        piece = [piece for piece in pieces if piece in items_1]
        piece_eaten = [piece for piece in pieces if piece in items_2]
        self.delete(piece_eaten)
        square_1 = [square for square in squares if square in items_1]
        square_2 = [square for square in squares if square in items_2]
        coords_1 = self.coords(square_1)
        coords_2 = self.coords(square_2)
        delta = coords_2[0] - coords_1[0], coords_2[1] - coords_1[1]
        self.move(piece, delta[0], delta[1])
        tags = [names[1], 'piece']
        self.itemconfigure(piece, tag=tags)
        self._draw_mask(names[1])
        self.chess_state.update(move)
        self.chess_states = self.chess_states[:self.turn + 1]
        self.chess_states.append(deepcopy(self.chess_state))
        self.turn += 1
        self.last_name = None

    def _on_click(self, _, name):
        if self.last_name is None:
            if self.chess_state[name] is None:
                return
            if not self._is_current_player(self.chess_state[name]):
                return
            self._delete_mask(self.chess_state['player'])
            self.last_name = name
            self._draw_mask(name)
            return
        if self.chess_state[name] is None or \
            not self._is_current_player(self.chess_state[name]):
            move = self.last_name + name
            if self._is_valid_move(move):
                self._move(move)
            return
        if self._is_current_player(self.chess_state[name]):
            self.last_name = name
            self.delete('mask')
            self._draw_mask(name)
            return
        print('Not a partition!')

    def _reset_masks(self):
        for player in 'bw':
            self._delete_mask(player)
        move = self.chess_state['moves'][-1]
        self._draw_mask(move[:2], 'flip_player')
        self._draw_mask(move[-2:], 'flip_player')

    def _setup_chessmen(self):
        for (_, xname), (_, yname) in Constant.iter_chessboard_id_name:
            name = xname + yname
            piece = self.chess_state[name]
            if piece is not None:
                image = self.images[piece]
                tags = [name, 'piece']
                self._create_image_at_square(name, image=image, tag=tags)

    def _setup_widgets(self):
        grid_x = [60 + 42*i for i in range(9)]
        grid_y = [65 + 42*i for i in range(10)]
        self._draw(grid_x, grid_y)
        self._setup_square(grid_x, grid_y)
        self._setup_chessmen()

    def _setup_square(self, grid_x, grid_y):
        for (xid, xname), (yid, yname) in Constant.iter_chessboard_id_name:
            name = xname + yname
            tags = [name, 'square']
            x1, y1 = grid_x[xid] - 21, grid_y[yid] - 21 # pylint: disable=C0103
            x2, y2 = grid_x[xid] + 21, grid_y[yid] + 21 # pylint: disable=C0103

            self.create_rectangle(x1, y1, x2, y2, tag=tags, width=0)

    def on_select(self, index):
        ''' React when the listbox's selection is changed.'''
        self.turn = index
        self.chess_state = deepcopy(self.chess_states[index])
        self.last_name = None
        masks = self.find_withtag('mask')
        for mask in masks:
            self.delete(mask)
        pieces = self.find_withtag('piece')
        for piece in pieces:
            self.delete(piece)
        self._setup_chessmen()
        self._reset_masks()

class ChessManual(tk.LabelFrame):
    ''' Show the chess menual.'''
    def __init__(self, root, images):
        super().__init__(root, text='棋谱', font=('楷体', 12),
                         borderwidth=2, relief=tk.RIDGE)
        self.root = root
        self.images = images
        self.listbox = None

        self._setup_widgets()

    def _on_click(self, flag):
        ''' Valid flags are: '--', '-', '+', '++'.'''
        try:
            index = int(self.listbox.curselection()[0])
        except IndexError:
            index = 0
        total = self.listbox.size()
        if flag == '--':
            self._set_selection(0)
            self._on_select()
        elif flag == '-':
            self._set_selection(max((index - 1, 0)))
            self._on_select()
        elif flag == '+':
            self._set_selection(min((index + 1, total - 1)))
            self._on_select()
        elif flag == '++':
            self._set_selection(tk.END)
            self._on_select()

    def _on_select(self, _=None):
        try:
            index = int(self.listbox.curselection()[0])
            self.root.chess_board.on_select(index)
        except IndexError:
            pass

    def _set_selection(self, index):
        self.listbox.focus_set()
        self.listbox.selection_clear(0, tk.END)
        self.listbox.activate(index)
        self.listbox.selection_set(index)
        self.listbox.see(index)

    def _setup_buttons(self):
        frame = tk.Frame(self)
        frame.pack()
        tk.Button(frame, image=self.images['most-left'], relief=tk.FLAT,
                  command=lambda: self._on_click('--')).grid(
                      row=0, column=0, padx=2)
        tk.Button(frame, image=self.images['left'], relief=tk.FLAT,
                  command=lambda: self._on_click('-')).grid(
                      row=0, column=1, padx=2)
        tk.Button(frame, image=self.images['right'], relief=tk.FLAT,
                  command=lambda: self._on_click('+')).grid(
                      row=0, column=2, padx=2)
        tk.Button(frame, image=self.images['most-right'], relief=tk.FLAT,
                  command=lambda: self._on_click('++')).grid(
                      row=0, column=3, padx=2)

    def _setup_listbox(self):
        self.listbox = tk.Listbox(self, width=16, font=('楷体', 12))
        vsb = tk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=vsb.set)
        self.listbox.pack(expand=True, fill=tk.Y)
        self.listbox.insert(tk.END, ' ' * 5 + '初始局面')
        self._set_selection(0)
        self.listbox.bind('<<ListboxSelect>>', self._on_select)

    def _setup_widgets(self):
        self._setup_listbox()
        self._setup_buttons()

    def insert_move(self, chess_state, turn, move):
        ''' Add a new move to the listbox.'''
        self.listbox.delete(turn + 1, tk.END)
        self.listbox.insert(
            tk.END,
            func.format_round(chess_state['round'], chess_state['player']) + \
            func.to_chinese_format(chess_state, move))
        self._set_selection(tk.END)

class ChessState(dict):
    ''' A dictionary of the form like "coordinate: piece".'''
    def __init__(self, fen=None):
        super().__init__()
        self['moves'] = []
        self._load_fen(fen)

    def _change_player(self):
        self['player'] = func.flip_player(self['player'])

    def _load_fen(self, fen):
        self['fen'] = fen if fen is not None else Constant.initial_fen
        self['init_fen'] = self['fen']
        fen_list = self['fen'].split()
        fen_0 = fen_list[0]
        self['player'] = fen_list[1]
        self['round'] = int(fen_list[5])
        x, y, xmax, ymax = 0, 0, 8, 9 # pylint: disable=C0103
        xlist, ylist = list('abcdefghi'), list('9876543210')
        for item in fen_0:
            if item.isdigit():
                for _ in range(int(item)):
                    if x > xmax:
                        raise IndexError('Index_x out of range.')
                    name = xlist[x] + ylist[y]
                    self[name] = None
                    x += 1 # pylint: disable=C0103
            if item == '/':
                x, y = 0, y + 1 # pylint: disable=C0103
                if y > ymax:
                    raise IndexError('Index_y out of range.')
            if item.isalpha():
                if x > xmax:
                    raise IndexError('Index_x out of range.')
                if y > ymax:
                    raise IndexError('Index_y out of range.')
                name = xlist[x] + ylist[y]
                self[name] = item
                x += 1 # pylint: disable=C0103

    def _update_fen(self):
        fen_0 = ''
        xlist, ylist = list('abcdefghi'), list('9876543210')
        count_empty = 0
        for yname in ylist:
            for xname in xlist:
                name = xname + yname
                if self[name] is None:
                    count_empty += 1
                    continue
                if count_empty != 0:
                    fen_0 += str(count_empty)
                    count_empty = 0
                fen_0 += self[name]
            if count_empty != 0:
                fen_0 += str(count_empty)
                count_empty = 0
            if yname != '0':
                fen_0 += '/'
        self['fen'] = ' '.join(
            [fen_0, self['player'], '-', '-', '0', str(self['round'])])

    def game_to_string(self):
        ''' Convert the game to a string.'''
        return ';'.join((self['init_fen'], ' '.join(self['moves'])))

    def update(self, move):
        ''' Update the chess state with the given move.'''
        self['moves'].append(move)
        names = move[:2], move[-2:]
        self[names[0]], self[names[1]] = None, self[names[0]]
        if self['player'] == 'b':
            self['round'] += 1
        self._change_player()
        self._update_fen()

class ChineseChess(tk.Tk):
    ''' A simple chinese chess program.'''
    def __init__(self, **kwargs):
        ''' Initialize.'''
        super().__init__()
        self._setup_widgets(**kwargs)
        self._bind_events()

    def _add_menu(self, menu):
        ''' Add the menu.'''
        menu(self)

    def _bind_events(self):
        self.bind('<Motion>', self._on_motion)
        self.protocol('WM_DELETE_WINDOW', self._on_closing)

    def _on_closing(self):
        answer = askyesnocancel('Quit', 'Do you want to save the chess manual?')
        if answer is None:
            pass
        elif answer is True:
            sys.stdout.write(self.chess_board.chess_states[-1].game_to_string())
            sys.stdout.flush()
            self.destroy()
            sys.exit(0)
        elif answer is False:
            sys.stdout.write('不重要吧')
            sys.stdout.flush()
            self.destroy()
            sys.exit(0)

    def _on_motion(self, event):
        if event.widget == self.chess_board:
            self.docs.configure(text='在棋盘内行棋以记录棋谱.')
        elif event.widget in (self.chess_manual, self.chess_manual.listbox):
            self.docs.configure(
                text='若要修改某步棋, 可以选择那步棋之前的一步棋, ' + \
                     '棋局便会变回当时的局面, 之后再重新行棋即可.')

    def _setup_widgets(self, **kwargs):
        ''' The interface.'''
        # self.geometry = '1920x1080'
        # self.state('zoomed')
        self.title('Chinese Chess')
        # self._add_menu(MyMenu)

        images = Images()
        self.chess_manual = ChessManual(self, images)
        self.chess_manual.grid(row=0, column=1, sticky=tk.NS)
        self.chess_board = Chessboard(self, images, **kwargs)
        self.chess_board.grid(row=0, column=0)
        self.docs = Docs(self)
        self.docs.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

class Docs(tk.Label):
    ''' Display the docstring of widgets.'''
    def __init__(self, root):
        super().__init__(root, font=('楷体', 10),
                         borderwidth=2, relief=tk.RIDGE)

class Images(dict):
    ''' Preload the images.'''
    def __init__(self):
        super().__init__()
        dirname = os.path.dirname(os.path.abspath(__file__))
        self._load_images(dirname + '/resources', 'png')

    def _load_images(self, path, extension):
        files = os.listdir(path)
        for file in files:
            file_path = '/'.join([path, file])
            if os.path.isdir(file_path):
                self._load_images(file_path, extension)
            else:
                name = os.path.splitext(os.path.split(file_path)[-1])[0]
                extension = os.path.splitext(file_path)[-1][1:]
                if extension == 'png':
                    if re.match('[bw][abcknpr]', name) is not None:
                        if name[0] == 'b':
                            name = name[1]
                        else:
                            name = name[1].capitalize()
                    self[name] = tk.PhotoImage(file=file_path)

class MyMenu():
    ''' A menu bar.'''
    def __init__(self, root):
        ''' Initialize.'''
        self.menu_bar = tk.Menu(root)

        # The file menu.
        menu_file = tk.Menu(self.menu_bar, tearoff=0)
        menu_file.add_command(label='Open')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Save')
        menu_file.add_separator()
        menu_file.add_command(label='Quit', command=root.quit)

        # The help menu.
        menu_help = tk.Menu(self.menu_bar, tearoff=0)
        menu_help.add_command(label='About')

        # Add menus to the menu bar.
        self.menu_bar.add_cascade(label="File", menu=menu_file)
        self.menu_bar.add_cascade(label="Help", menu=menu_help)

        # Load the menu bar.
        root.configure(menu=self.menu_bar)

if __name__ == '__main__':
    main(sys.argv[1:])
