# Author: Justin David Todd
# Last Modified: 02/04/2021
# Description: This class holds the internal settings for the GarudaGame
#   such as window size, FPS, background, etc.
import pygame
from ships import Player, Enemy


class GarudaGame:
    """
    Creates a playable ship-shooting game.
    Defines creation of player, laser, and enemy objects,
      game backgrounds, level sequence, and level configurations.
    """

    def __init__(self):
        """Initializes default window configurations."""

        # Stores window size
        self._window_width = 800
        self._window_height = 800

        # Dictionary of Game Backgrounds
        self._backgrounds = {
            "bg_default": pygame.transform.scale(pygame.image.load("assets/starlight_bg.png"),
                                                 (self._window_width, self._window_height)),
        }

        # General Display Attributes
        self._background = self._backgrounds["bg_default"]
        self._fps = 60
        self._current_level = 0

        # Stores Enemies, Enemy Lasers, Player Lasers and Levels
        self._enemies = []
        self._enemy_lasers = []
        self._player_lasers = []
        self._level_sequence = []

    # Get Methods
    def get_background(self):
        """Returns the current game background"""
        return self._background

    def get_fps(self):
        """Returns the game's fps"""
        return self._fps

    def get_width(self):
        """Returns the width of the game window."""
        return self._window_width

    def get_height(self):
        """Returns the height of the game window"""
        return self._window_height

    def get_current_level(self):
        """Returns the current level"""
        return self.get_current_level()

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

    # Set Methods
    def set_background(self, image_name):
        """Takes an image and sets the background to that image."""
        self._background = self._backgrounds[image_name]

    def resize_window(self, width, height):
        """Takes two integers, width and height, and resizes the window to those dimensions."""
        self._window_width = width
        self._window_height = height

    # Other Methods
    def next_level(self):
        """Loads the next level in level_sequence and increments the current level."""
        self._level_sequence[self._current_level]()
        if self._current_level < len(self._level_sequence)-1:
            self._current_level += 1

    def spawn_player(self):
        """Creates a new Player object in the lower center of the screen."""
        # Creates player ship at the center bottom of the screen
        #   and passes player_lasers as array to store lasers fired.
        player = Player(0, 0, self._player_lasers, 100)
        player.set_x(self._window_width / 2 - player.get_width() / 2)
        player.set_y(self._window_height - 100)
        # Informs Player object of game window dimensions
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

    # Collection of Spawn Patterns
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

    # Collection of Game Levels
    def level_one(self):
        """spawns enemies for level 1"""
        # WAVE 1
        self.spawn_row(-100, "Squid", "Block")
        self.spawn_row(-164, "Squid")
        # WAVE 2
        self.spawn_row(200, "Squid")
        self.spawn_row(264, "Squid")

    def level_two(self):
        """spawns enemies for level 1"""
        self.spawn_block(200, "Metal1")

    def load_levels(self):
        """Loads the order that the player will play through each level"""
        self._level_sequence.append(self.level_one)
        self._level_sequence.append(self.level_two)
