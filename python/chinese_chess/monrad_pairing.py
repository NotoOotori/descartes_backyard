''' The program for Monrad pairing algorithm of Swiess-system tournament.
    The syntax of monrad_pairing command:
        monrad_pairing { -p | --previous-pairings } <previous_pairings>

        <previous_pairings> ::=
            { <player_id>: [ { [*] <opponent_id> <round_score> } [ ,...n ] ] } [ ;...n ]
        where '*' stands for moving first.

    Return:
        <table> [ ,...n ]

        <table> ::=
            <red_id> <black_id>
'''
import getopt
import sys
from copy import deepcopy as copy
from itertools import permutations
from random import randint


def main(argv):
    ''' Main function.'''
    help_str = '\n'.join([
        'The syntax of monrad_pairing command:',
        '    monrad_pairing { -p | --previous-pairings } <previous_pairings>',
        '',
        '    <previous_pairings> ::=',
        '        { <player_id>: [ { [*] <opponent_id> <round_score> } [ ,...n ] ] } [ ;...n ] ',
        '    where "*" stands for moving first.'])
    kwargs = {}
    try:
        opts, _ = getopt.getopt(argv, 'hp:', ['help', 'previous-pairings='])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                sys.stdout.write(help_str)
                sys.stdout.flush()
                sys.exit(0)
            elif opt in ('-p', '--previous-pairings'):
                kwargs['previous_pairings'] = arg
        if 'previous_pairings' not in kwargs.keys():
            raise getopt.GetoptError('')
        pairings = monrad_pairing(
            Players.fromstring(kwargs['previous_pairings']), Pairings())
        pairing = pairings.optimize()
        sys.stdout.write(pairing.to_string())
        sys.stdout.flush()
        sys.exit(0)
    except getopt.GetoptError:
        sys.stdout.write(help_str)
        sys.stdout.flush()
        sys.exit(1)

def monrad_pairing(players, old_pairings=None):
    ''' Monrad pairing function of Swiess-system tournament.
        dfs!
        Return final pairing or the text 'Failure'.
    '''
    if old_pairings is None:
        old_pairings = Pairings()
    pairings = Pairings()
    if not old_pairings:
        new_pairings = pair_with_score(players, Pairing([]))
        pairings.extend(new_pairings)
    else:
        for pairing in old_pairings:
            tmp_players = copy(players)
            tmp_players.exclude_pairing(pairing)
            new_pairings = pair_with_score(tmp_players, pairing)
            pairings.extend(new_pairings)
    tmp_players = copy(players)
    if pairings:
        tmp_players.exclude_pairing(pairings[0])
        if not tmp_players:
            return pairings
    return monrad_pairing(players, pairings)

def pair_with_score(players, old_pairing):
    ''' Pair all people with the maximum score.
        Return the sorted pairing or the text 'Failure'.
    '''
    max_score = players.max_score
    max_score_players = players.with_score(max_score)
    tmp_pairings = Pairings([
        Pairing.from_players_list(pairing_comb) for pairing_comb in pairing_combinations(
            max_score_players)
        ]).select_min_remainings()
    pairings = Pairings()
    for tmp_pairing in tmp_pairings:
        try:
            tmp_old_pairing = copy(old_pairing)
            tmp_old_pairing.extend(tmp_pairing)
            remainings = tmp_pairing.kill_remainings(players.less_than_score(max_score))
            if not remainings:
                continue
            for remaining_pair in remainings:
                pairing = copy(tmp_old_pairing)
                pairing.extend(remaining_pair)
                pairings.append(pairing)
        except IndexError:
            pass
    return pairings

def pairing_combinations(players, old_combinations=None):
    ''' Return new pairing combinations of players.'''
    if old_combinations is None:
        old_combinations = [[]]
    if not players:
        return copy(old_combinations)
    tmp_player = players.pop(0)
    for old_combination in old_combinations:
        old_combination.append(tmp_player)
    del tmp_player
    if not players:
        return copy(old_combinations)
    combinations = []
    for index, player in enumerate(players):
        tmp_players = copy(players)
        tmp_players.pop(index)
        tmp_combinations = copy(old_combinations)
        for tmp_combination in tmp_combinations:
            tmp_combination.append(player)
        combinations.extend(
            pairing_combinations(tmp_players, tmp_combinations))
    return combinations

class GameRecord(dict):
    ''' A class for a single game record for one player.'''
    def __init__(self, pairing_str):
        super().__init__()
        if pairing_str[0] == '*':
            self['first'] = True
            pairing_str = pairing_str[1:].strip()
        else:
            self['first'] = False
        self['opponent'], self.score = [
            string.strip() for string in pairing_str.split(' ')]
        self.score = int(self.score)

class GamePairing():
    ''' Attribute: red_player, black_player.'''
    def __init__(self, red_player, black_player):
        self.red_player = red_player
        self.black_player = black_player

    def __getattr__(self, name):
        if name == 'value':
            value = 0
            if self.red_player.pid == '-1':
                return -1000
            if self.black_player.pid == '-1':
                return 1000
            if self.red_player.firsts <= self.red_player.lasts:
                pass
            elif self.red_player.firsts - self.red_player.lasts == 1:
                pass
            elif self.red_player.firsts - self.red_player.lasts > 1:
                value -= 50
            if self.red_player.straight_firsts == 0:
                pass
            elif self.red_player.straight_firsts == 1:
                value -= 5
            elif self.red_player.straight_firsts >= 2:
                value -= 50

            if self.black_player.lasts <= self.black_player.firsts:
                pass
            elif self.black_player.lasts - self.black_player.firsts == 1:
                pass
            elif self.black_player.lasts - self.black_player.firsts > 1:
                value -= 50
            if self.black_player.straight_lasts == 0:
                pass
            elif self.black_player.straight_lasts == 1:
                value -= 5
            elif self.black_player.straight_lasts >= 2:
                value -= 50

            return value
        raise AttributeError

    def flip(self):
        ''' Return flipped game pairing.'''
        return GamePairing(self.black_player, self.red_player)

    def is_valid(self):
        ''' Judge whether the game_pairing is valid.'''
        return self.black_player.pid not in self.red_player.opponents

class Pairing(list):
    ''' List of game_pairings.'''
    def __init__(self, game_pairings, remaining_players=None):
        super().__init__()
        if remaining_players is None:
            remaining_players = []
        self.extend(game_pairings)
        self.remaining_players = remaining_players

    def __getattr__(self, name):
        if name == 'remainings':
            return len(self.remaining_players)
        if name == 'players':
            players = Players([])
            for game_pairing in self:
                players.extend(
                    [game_pairing.red_player, game_pairing.black_player])
            return players
        if name == 'value':
            return sum([game_pairing.value for game_pairing in self])
        raise AttributeError

    @classmethod
    def from_players_list(cls, players):
        ''' Initialize pairing from a list of players.'''
        game_pairings, remaining_players = [], []
        while len(players) >= 2:
            red_player, black_player = players.pop(0), players.pop(0)
            game_pairing = GamePairing(red_player, black_player)
            if game_pairing.is_valid():
                game_pairings.append(game_pairing)
            else:
                remaining_players.extend([red_player, black_player])
        remaining_players.extend(players)
        return cls(game_pairings, remaining_players)

    def optimize(self):
        ''' Optimize game_pairings.
            No returns.
        '''
        for index, game_pairing in enumerate(self):
            game_pairing_value = game_pairing.value
            game_pairing_flip = game_pairing.flip()
            game_pairing_flip_value = game_pairing_flip.value
            if randint(0, 1) == 1:
                game_pairing_value -= 1
            else:
                game_pairing_flip_value -= 1
            if game_pairing_value < game_pairing_flip_value:
                self[index] = game_pairing_flip

    def kill_remainings(self, players):
        ''' Pair the remaining players.
            Parameter players should not include greatest-score ones.
        '''
        try:
            score = players.max_score
        except ValueError:
            score = 0
        while True:
            tmp_players = players.no_less_than_score(score)
            if score < -1:
                return False
            if score == -1:
                tmp_players.append(Player('-1: -1 -1'))
            if len(tmp_players) < self.remainings:
                score -= 1
                continue
            pairings = Pairings()
            for pmt_tmp_players in permutations(tmp_players, self.remainings):
                pairing = Pairing([])
                for remain, player in zip(self.remaining_players, pmt_tmp_players):
                    pairing.append(GamePairing(remain, player))
                if pairing.is_valid():
                    pairings.append(pairing)
            if pairings:
                return pairings
            score -= 1
            continue

    def is_valid(self):
        ''' Judge whether the pairing is valid.'''
        return False if [
            game_pairing.is_valid() for game_pairing in self
            ].count(False) else True

    def to_string(self):
        ''' Convert the pairing to string.'''
        return ','.join(['{} {}'.format(gs.red_player.pid, gs.black_player.pid) for gs in self])

class Pairings(list):
    ''' List of pairings.'''
    def __init__(self, pairings=None):
        super().__init__()
        if pairings is None:
            pairings = Pairing([])
        self.extend(pairings)

    def __getattr__(self, name):
        if name == 'min_remainings':
            return min(self, key=lambda p: p.remainings).remainings
        raise AttributeError

    def optimize(self):
        ''' Optimize the pairings.
            Also return a random pairing among the best pairings.
        '''
        for pairing in self:
            pairing.optimize()
        self.sort(key=lambda p: p.value)
        max_value = self[0].value
        pairings_best = Pairings()
        for pairing in self:
            if pairing.value == max_value:
                pairings_best.append(pairing)
            else:
                break
        return pairings_best[randint(0, len(pairings_best) - 1)]

    def select_min_remainings(self):
        ''' Return the pairings with minimum remaining players.'''
        return Pairings([
            pairing for pairing in self if pairing.remainings == self.min_remainings])

class Player():
    ''' A class for one player.
        Attributes:
            firsts, firsts_lasts_list, games, lasts, opponents,
            score, stright_firsts, stright_lasts.
    '''
    def __init__(self, player_str):
        self.pid, pairings_str = [
            string.strip() for string in player_str.split(':')]
        self.pairings = []
        for pairing_str in pairings_str.split(','):
            pairing = GameRecord(pairing_str.strip())
            self.pairings.append(pairing)

    def __getattr__(self, name):
        if name == 'firsts':
            return self.firsts_lasts_list.count(True)
        if name == 'firsts_lasts_list':
            return [pairing['first'] for pairing in self.pairings]
        if name == 'games':
            return len(self.pairings)
        if name == 'lasts':
            return self.firsts_lasts_list.count(False)
        if name == 'opponents':
            return [pairing['opponent'] for pairing in self.pairings]
        if name == 'score':
            return sum([pairing.score for pairing in self.pairings])
        if name == 'straight_firsts':
            count = 0
            firsts_lasts_list = self.firsts_lasts_list
            try:
                while firsts_lasts_list.pop() is True:
                    count += 1
            except IndexError:
                pass
            return count
        if name == 'straight_lasts':
            count = 0
            firsts_lasts_list = self.firsts_lasts_list
            try:
                while firsts_lasts_list.pop() is False:
                    count += 1
            except IndexError:
                pass
            return count
        raise AttributeError('Class player doesn\'t have attribution of {}'.format(name))

class Players(list):
    ''' A class for all players.
        Attributes:
            max_score.
    '''
    def __init__(self, players):
        super().__init__()
        self.extend(players)

    def __getattr__(self, name):
        if name == 'max_score':
            return max(self, key=lambda p: p.score).score
        raise AttributeError

    @classmethod
    def fromstring(cls, players_str):
        ''' Initialize Players from a string.'''
        players = []
        for player_str in players_str.split(';'):
            players.append(Player(player_str.strip()))
        players.sort(key=lambda p: p.score)
        return cls(players)

    @classmethod
    def fromlist(cls, players):
        ''' Initialize Players from a list.'''
        players.sort(key=lambda p: p.score)
        return cls(players)

    def exclude_pairing(self, pairing):
        ''' Exclude paired players.'''
        pids = [player.pid for player in pairing.players]
        for player in self.copy():
            if player.pid in pids:
                self.remove(player)

    def with_score(self, score):
        ''' Return the players with the specified score.'''
        return Players.fromlist(
            [player for player in self if player.score == score])

    def less_than_score(self, score):
        ''' Return the players less than the specified score.'''
        return Players.fromlist(
            [player for player in self if player.score < score])

    def no_less_than_score(self, score):
        ''' Return the players no less than the specified score.'''
        return Players.fromlist(
            [player for player in self if player.score >= score])

if __name__ == '__main__':
    main(sys.argv[1:])
    #Player('-1: -2 -1')
    #PLAYERS = Players.fromstring("1: *2 2; 2: 1 0; 3: *4 1; 4: 3 1; 5: *-1 2")
    #PAIRINGS = monrad_pairing(PLAYERS, Pairings())
    #for PAIRING in PAIRINGS:
    #    for GAMEPAIRING in PAIRING:
    #        print('{} vs {}'.format(GAMEPAIRING.red_player.pid, GAMEPAIRING.black_player.pid))
    #    print('')
