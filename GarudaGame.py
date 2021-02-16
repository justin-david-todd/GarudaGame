# Author: Justin David Todd
# Last Modified: 01/31/2021
# Description: This class stores and initializes all existing player ships,
# enemy ships, and lasers. Keeps track of current score.
# Contains functions for enemy spawn patterns and constructed levels
# for user to play.

from ships import *
import random


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

        # Stores Current Score
        self._score = 0

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
        return self._current_level

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

    def get_score(self):
        """Returns the current score"""
        return self._score

    # Set Methods
    def set_background(self, image_name):
        """Takes an image and sets the background to that image."""
        self._background = self._backgrounds[image_name]

    def resize_window(self, width, height):
        """Takes two integers, width and height, and resizes the window to those dimensions."""
        self._window_width = width
        self._window_height = height

    # Other Methods
    def amend_score(self, num):
        """Takes an integer value and adds it to the current score."""
        self._score += num

    def next_level(self):
        """Loads the next level in level_sequence and increments the current level."""
        if self._current_level < len(self._level_sequence) - 1:
            self._level_sequence[self._current_level]()
        else:
            self._level_sequence[-1]()
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
    def spawn_row(self, distance, species, species2=None, adjust=None):
        """
        Takes a distance in pixels and a species.
        Takes an optional second species to alternate enemies.
        Takes an optional fourth argument to set x coordinate of left most spawn.
        Spawns a central row of 10 enemies of that species
         starting that distance above the screen.
        (Negative distance spawns enemies on screen)
        """
        if species2 is None:
            species2 = species
        left_indent = 64
        spacing = 64
        num_enemies = 10

        # Optional adjust of x coordinate
        if adjust is not None:
            left_indent = adjust

        for spawn in range(0, num_enemies):
            if spawn % 2 == 0:
                self.spawn_enemy(left_indent + spacing * spawn, -distance, species)
            else:
                self.spawn_enemy(left_indent + spacing * spawn, -distance, species2)

    def spawn_column(self, distance, col, species, species2=None):
        """
        Takes a distance in pixels, an x coordinate, and a species.
        Takes an optional second species to alternate enemies.
        Spawns a column positioned at the coordinate of 10 enemies of that species
         starting that distance above the screen.
        (Negative distance spawns enemies on screen)
        """
        if species2 is None:
            species2 = species
        left_indent = col
        spacing = 64
        num_enemies = 10
        for spawn in range(0, num_enemies):
            if spawn % 2 == 0:
                self.spawn_enemy(left_indent, -distance - spacing * spawn, species)
            else:
                self.spawn_enemy(left_indent, -distance - spacing * spawn, species2)

    def spawn_split(self, distance, species, species2=None):
        """
        Takes a distance in pixels and a species.
        Takes an optional second species to alternate enemies.
        Spawns a central row of 10 enemies of that species
         starting that distance above the screen.
        (Negative distance spawns enemies on screen)
        """
        if species2 is None:
            species2 = species
        left_indent = 64*2
        spacing = 64
        num_enemies = 8
        for spawn in range(0, num_enemies):
            if spawn != 3 and spawn != 4:
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

    def spawn_v(self, distance, species, species2=None):
        """
        Takes a distance in pixels and a species.
        Takes an optional second species to alternate enemies.
        Spawns 11 enemies of the specified type in a "V" shape
         starting that distance above the screen.
        (Negative distance spawns enemies on screen)
        """
        if species2 is None:
            species2 = species
        left_indent = 64
        spacing = 64
        num_enemies = 11
        # Adjusts drop height to match entered distance.
        distance += 64 * (num_enemies//2 + 1)
        # Spawns front enemy and enemies on descending part of "V"
        for spawn in range(0, num_enemies//2+1):
            if spawn % 2 == 0:
                self.spawn_enemy(left_indent + spacing * spawn, -distance + 64*spawn, species)
            else:
                self.spawn_enemy(left_indent + spacing * spawn, -distance + 64*spawn, species2)

        # Preserves location of front of "V"
        last_x = left_indent+spacing*(num_enemies//2)
        last_y = -distance+64*(num_enemies//2)

        # Spawns enemies on ascending part of "V"
        for spawn in range(1, num_enemies//2+1):
            if spawn % 2 == 1:
                self.spawn_enemy(last_x + spacing * spawn, last_y - 64*spawn, species2)
            else:
                self.spawn_enemy(last_x + spacing * spawn, last_y - 64 * spawn, species)

    def spawn_random_rain(self, distance, quantity, species):
        """
        Takes a distance value, quantity, and a species. spaces the specified
        quantity of single enemies of that species about 800px apart (height),
        assigning them a random x coordinate.
        Starting distance of first enemy is specified distance.
        """
        random.seed()
        ship_width = Enemy(0, 0, [], species).get_width()
        spacing = 800
        for spawn in range(quantity):
            self.spawn_enemy(random.randint(0, self.get_width()-ship_width), -distance-spacing*spawn, species)

    def spawn_centipede_left(self, distance, head, body1, body2, length=None):
        """ Takes a spawn distance, a head, and two body part enemies.
        Spawns a left-facing horizontal centipede with a head and two kinds of body parts.
        Takes an optional fourth argument to specify the centipede's number of segments.
        Default number of segments is 7.
        """
        left_indent = 64
        spacing = 64
        segments = 7

        if length is not None:
            segments = length

        self.spawn_enemy(left_indent, -distance, head)
        for spawn in range(1, segments+1):
            if spawn % 2 == 0:
                self.spawn_enemy(left_indent + spacing * spawn, -distance, body1)
            else:
                self.spawn_enemy(left_indent + spacing * spawn, -distance, body2)

    def spawn_centipede_right(self, distance, head, body1, body2, length=None):
        """ Takes a spawn distance, a head, and two body part enemies.
        Spawns a right-facing horizontal centipede with a head and two kinds of body parts.
        Takes an optional fourth argument to specify the centipede's number of segments.
        Default number of segments is 7.
        """
        right_indent = 128
        spacing = 64
        segments = 7

        if length is not None:
            segments = length

        self.spawn_enemy(self.get_width()-right_indent, -distance, head)
        for spawn in range(1, segments+1):
            if spawn % 2 == 0:
                self.spawn_enemy(self.get_width()-right_indent - spacing * spawn, -distance, body1)
            else:
                self.spawn_enemy(self.get_width()-right_indent - spacing * spawn, -distance, body2)

    # Collection of Game Levels
    # Waves should be spaced by a distance of 600 to 800
    def level_one(self):
        """spawns enemies for level 1"""
        # WAVE 1
        self.spawn_split(64, "Squid")
        self.spawn_row(128, "Squid")

        # WAVE 2
        self.spawn_row(828, "Squid", "Block")
        self.spawn_split(892, "Squid")
        self.spawn_split(1020, "Squid")
        self.spawn_random_rain(1020, 3, "ArrowStealth")

        # WAVE 3
        self.spawn_random_rain(1720, 5, "ArrowStealth")
        self.spawn_random_rain(1740, 5, "ArrowStealth")
        self.spawn_random_rain(1760, 5, "ArrowStealth")
        self.spawn_split(1720, "Block")
        self.spawn_split(1784, "Squid")
        self.spawn_random_rain(1912, 2, "Metal1")
        self.spawn_random_rain(1978, 2, "Metal1")

    def level_two(self):
        """spawns enemies for level 2"""
        # WAVE 1
        self.spawn_split(64, "Squid")
        self.spawn_split(128, "Squid")
        self.spawn_split(128+64, "Metal1")
        self.spawn_random_rain(128, 5, "ArrowStealth")
        self.spawn_random_rain(148 * 4, 5, "ArrowStealth")
        self.spawn_random_rain(168 * 7, 5, "ArrowStealth")

        # WAVE 2
        self.spawn_centipede_left(400, "CentiheadPanda", "CentiBlue", "CentiGreen")
        self.spawn_centipede_right(464, "CentiheadRed", "CentiPurple", "CentiRed")
        self.spawn_column(1020, 64, "FlappyWhite")
        self.spawn_column(1020, 800-128, "FlappyWhite2")
        self.spawn_column(1920, 128, "FlappyWhite")
        self.spawn_column(1920, 800 - 192, "FlappyWhite2")
        self.spawn_v(1420, "Block")
        self.spawn_v(1620, "Block")

    def level_three(self):
        """spawns enemies for level 3"""
        self.spawn_enemy(368, -64, "Hammer")
        self.spawn_enemy(300-64, -664, "Hammer")
        self.spawn_enemy(500, -664, "Hammer")
        self.spawn_random_rain(800, 10, "Hammer")
        self.spawn_random_rain(832, 10, "Hammer")
        self.spawn_random_rain(864, 10, "Hammer")
        self.spawn_random_rain(880, 10, "Hammer")
        self.spawn_random_rain(900, 10, "Hammer")

    def level_four(self):
        """spawns enemies for level 4"""
        self.spawn_centipede_right(0, "CentiheadDud", "CentiheadDud", "CentiheadDud")
        self.spawn_centipede_right(64, "CentiheadDud", "CentiheadDud", "CentiheadDud")
        self.spawn_v(128, "CentiheadDud")

    def level_heck(self):
        """spawns an endless supply of impossible enemies."""
        # Wave 1
        self.spawn_block(64, "Squid")
        self.spawn_random_rain(820, 5, "ArrowStealth")

        # Wave 2
        self.spawn_centipede_right(664, "CentiheadDud", "CentiheadDud", "CentiheadDud", 10)
        self.spawn_centipede_right(728, "CentiheadDud", "CentiheadDud", "CentiheadDud", 10)
        self.spawn_centipede_right(728+64, "CentiheadDud", "CentiheadDud", "CentiheadDud", 10)
        self.spawn_random_rain(780, 6, "Metal1")
        self.spawn_random_rain(820, 6, "Metal1")

        # Wave 3
        self.spawn_block(3020, "Block")

    def load_levels(self):
        """Loads the order that the player will play through each level"""
        # self._level_sequence.append(self.level_one)
        # self._level_sequence.append(self.level_two)
        self._level_sequence.append(self.level_three)
        self._level_sequence.append(self.level_four)
        self._level_sequence.append(self.level_heck)
