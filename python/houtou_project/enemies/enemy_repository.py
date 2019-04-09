''' The class EnemyRepo'''
from enemies.bat_girl import BatGirl


class EnemyRepo():
    ''' Store instances of all enemies.'''
    def __init__(self, screen):
        self.bat_girl = BatGirl(screen, 'resources/player.png',
                                (screen.get_rect().centerx, 60), 150000)
