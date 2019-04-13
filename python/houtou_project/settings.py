''' The Settings class'''
class Settings():
    ''' Store all settings of the game.'''
    # TODO: Read settings from ini or json file.
    def __init__(self):
        ''' Initialize the settings'''
        # Set the screen settings.
        self.screen_width, self.screen_height = (1024, 768)
        self.bg_color = (40, 40, 40)

        # Set the path of player's image.
        self.player_image_path = 'resources/player.png'
        # Set the size and color of the collision box.
        self.collision_box_radius = 6
        self.collision_box_width = 3
        self.collision_box_color_edge = (255, 0, 0)
        self.collision_box_color_inside = (255, 255, 255)
        # Set the player's speed.
        self.player_speed = 16

        # Set the maxium frames per second.
        self.fps = 60
