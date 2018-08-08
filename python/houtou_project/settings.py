""" The Settings class"""
class Settings():
    """ All settings of the game"""
    def __init__(self):
        """ Initialize the settings"""
        # Set the screen settings.
        self.screen_width, self.screen_height = (1024, 768)
        self.bg_color = (40, 40, 40)

        # Set the path of player's image
        self.player_image_path = 'images/player.png'

        # Set the maxium frames per second
        self.fps = 150
