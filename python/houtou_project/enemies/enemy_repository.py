""" The class EnemyRepo"""
from enemies.bat_girl import BatGirl


class EnemyRepo(dict):
    """ Store instances of all enemies. """
    def __init__(self, screen):
        super().__init__()
        self["bat_girl"] = BatGirl(screen, 'resources/player.png',
                                   (screen.get_rect().centerx, 60), 150000)

    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
        raise AttributeError(
            "Attribute {} not found in EnemyRepo.".format(name))
