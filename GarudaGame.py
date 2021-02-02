# Author: Justin David Todd
# Last Modified: 01/31/2021
# Description: This class holds the internal settings for the GarudaGame
#   such as window size, FPS, background, etc.
# Testing changes to Title Features
from ships import *


class GarudaGame:
    """Holds GarudaGame configurations such as window size, FPS, and images."""

    def __init__(self):
        """Initializes default window configurations."""
        # General Display Attributes
        self._window_width = 800
        self._window_height = 800
        self._fps = 60
        self._window = pygame.display.set_mode((self._window_width, self._window_height))
        self._current_level = 0

        # Dictionary on Image assets
        self._image = {
            "bg_default": pygame.transform.scale(pygame.image.load("assets/starlight_bg.png"),
                                                 (self._window_width, self._window_height)),

            # Sprites
            # Player Images - image file should be 64x64 pixels
            "main_ship": pygame.image.load("assets/main_ship.png"),

            # Enemy Images - image file should be 32x32 pixels
            "blue_baddy": pygame.image.load("assets/baddy_1.png"),
            "red_baddy": pygame.image.load("assets/baddy_2.png")
        }

        # Dictionary of used fonts
        self._font = {
            "main": pygame.font.SysFont('comicsansms', 50),
            "lost": pygame.font.SysFont('comicsansms', 80)
        }

        # background, icon, and caption contents
        self._background = self._image["bg_default"]
        self._icon = self._image["blue_baddy"]
        self._caption = "Garuda"

        # Lists holding Player Lasers, Enemy Lasers, and Enemies (for iterating through groups)
        self._enemies = []
        self._enemy_lasers = []
        self._player_lasers = []
        self._level_sequence = []

    def image(self, image_name):
        """
        Takes an image name and retrieves the image of that name.
        """
        return self._image[image_name]

    def font(self, font_name):
        """
        Takes a font name and retrieves the image of that name.
        """
        return self._font[font_name]

    def get_width(self):
        """Returns the width of the game window."""
        return self._window_width

    def get_height(self):
        """Returns the height of the game window"""
        return self._window_height

    def get_fps(self):
        """Returns the game's fps"""
        return self._fps

    def get_icon(self):
        """Returns the game's icon"""
        return self._icon

    def get_current_level(self):
        """Returns the current level"""
        return self.get_current_level()

    def get_caption(self):
        """Returns the game's caption"""
        return self._caption

    def get_window(self):
        """Returns the game's window."""
        return self._window

    def get_background(self):
        """Returns the game's background"""
        return self._background

    def get_enemies(self):
        """Returns the list of all active enemies"""
        return self._enemies

    def get_enemy_lasers(self):
        """Returns the list of all active enemies"""
        return self._enemy_lasers

    def get_player_lasers(self):
        """Returns the list of all active enemies"""
        return self._player_lasers

    def get_level_sequence(self):
        """Retrieves the level sequence"""
        return self._level_sequence

    def set_icon(self, image_name):
        """Takes an image name and sets the icon to that image."""
        self._icon = self.image(image_name)
        pygame.display.set_icon(system.get_icon())

    def set_caption(self, string):
        """Takes a string and sets the caption to that string"""
        self._caption = string
        pygame.display.set_caption(system.get_caption())

    def resize_window(self, width, height):
        """Takes two integers, width and height, and resizes the window to those dimensions."""
        self._window_width = width
        self._window_height = height

    def set_background(self, image_name):
        """Takes an image and sets the background to that image."""
        self._background = pygame.transform.scale(self._image[image_name],
                                                 (self._window_width, self._window_height)),

    def display_decor(self):
        """Displays game icon at start in corner of game window."""
        pygame.display.set_icon(self.get_icon())
        pygame.display.set_caption(self.get_caption())

    def next_level(self):
        self._level_sequence[self._current_level]()
        self._current_level += 1

    def spawn_player(self):
        """Creates a new Player object in the lower center of the screen."""
        # creates player ship at the center bottom of the screen.
        # passing player_lasers array to store lasers fired.
        player = Player(0, 0, self._player_lasers, 100)
        player.set_x(self._window_width / 2 - player.get_width() / 2)
        player.set_y(self._window_height - 100)
        # informs player of game window dimensions
        player.set_window(self._window_width, self._window_height)
        return player

    def spawn_enemy(self, x, y, species):
        """
        Takes an x coordinate, y coordinate, and species.
        Spawns a new enemy of that species at that location.
        Passes the enemy the laser attay to store lasers fired.
        Adds enemy to list of enemies.
        """
        enemy = Enemy(x, y, self._enemy_lasers, species)
        enemy.set_window(self._window_width, self._window_height)
        self._enemies.append(enemy)

    # spawn patterns
    def spawn_row(self, distance, species, species2=None):
        """
        Takes a distance in pixels and a species.
        Takes an optional second species to alternate enemies.
        Spawns a central row of 10 enemies of that species
         starting that distance above the screen.
        (Negative distance spawns enemies on screen)
        """
        if species2 is None:
            species2 = species
        left_indent = 64
        spacing = 64
        num_enemies = 10
        for spawn in range(0, num_enemies):
            if spawn % 2 == 0:
                self.spawn_enemy(left_indent + spacing * spawn, -distance, species)
            else:
                self.spawn_enemy(left_indent + spacing * spawn, -distance, species2)

    def spawn_block(self, distance, species, species2=None):
        """
        Takes a distance in pixels and a species.
        Spawns a central 10x10 enemies of that species
         starting that distance above the screen.
        (Negative distance spawns enemies on screen)
        """
        for row in range(10):
            self.spawn_row(distance, species, species2)
            distance += 64

    # Game Level Designs

    def level_one(self):
        """spawns enemies for level 1"""
        # WAVE 1
        self.spawn_row(-100, "squid")
        self.spawn_row(-164, "squid")
        self.spawn_row(200, "squid")
        self.spawn_row(264, "squid")

    def level_two(self):
        """spawns enemies for level 1"""
        self.spawn_block(200, "squid")

    def load_levels(self):
        """Loads the order that the player will play through each level"""
        self._level_sequence.append(self.level_one)
        self._level_sequence.append(self.level_two)
