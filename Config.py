# Author: Justin David Todd
# Last Modified: 02/04/2021
# Description: This Config class represents the running game console.
#   Holds system's "ON" status and stores/retrieves menu images, backgrounds,
#   window attributes, icons, fps, etc.
#   Music, Game saves and High scores would also be stored in this class.
import pygame
pygame.font.init()


class Config:
    """Holds system's ON status and stores and retrieves game saves."""

    def __init__(self):
        """Initializes attributes that store game running and save data"""
        self._system_on = True
        self._destination = "new_game"
        self._window_width = 800
        self._window_height = 800
        self._fps = 60
        self._window = pygame.display.set_mode((self._window_width, self._window_height))
        self._image = {
            "bg_default": pygame.transform.scale(pygame.image.load("assets/starlight_bg.png"),
                                                 (self._window_width, self._window_height)),

            # Sprites
            # Player Images - image file should be 64x64 pixels
            "main_ship": pygame.image.load("assets/main_ship.png"),
        }
        self._window = pygame.display.set_mode((self._window_width, self._window_height))
        self._background = self._image["bg_default"]
        self._icon = self._image["main_ship"]
        self._caption = "Garuda"

        self._font = {
            "main": pygame.font.SysFont('comicsansms', self.get_height()//16),
            "lost": pygame.font.SysFont('comicsansms', self.get_height()//10),
            "sub menu": pygame.font.SysFont('comicsansms', self.get_height()//12),
            "title": pygame.font.SysFont('comicsansms', self.get_height()//5)
        }

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

    def get_caption(self):
        """Returns the game's caption"""
        return self._caption

    def get_destination(self):
        """Returns selected screen"""
        return self._destination

    def get_window(self):
        """Returns the game's window."""
        return self._window

    def get_background(self):
        """Returns the game's background"""
        return self._background

    def get_image(self, image_name):
        """Takes an image name and returns the related image."""
        return self._image[image_name]

    def set_background(self, image_name):
        """Takes an image and sets the background to that image."""
        self._background = pygame.transform.scale(self._image[image_name],
                                                  (self._window_width, self._window_height))

    def set_destination(self, screen):
        """Takes a string and sets self._destination to that screen."""
        self._destination = screen

    def set_icon(self, image_name):
        """Takes an image name and sets the icon to that image."""
        self._icon = self._image[image_name]
        pygame.display.set_icon(self.get_icon())

    def set_caption(self, string):
        """Takes a string and sets the caption to that string"""
        self._caption = string
        pygame.display.set_caption(self.get_caption())

    def display_decor(self):
        """Displays game icon at start in corner of game window."""
        pygame.display.set_icon(self.get_icon())
        pygame.display.set_caption(self.get_caption())

    def resize_window(self, width, height):
        """Takes two integers, width and height, and resizes the window to those dimensions."""
        self._window_width = width
        self._window_height = height

    def font(self, font_name):
        """
        Takes a font name and retrieves the image of that name.
        """
        return self._font[font_name]

    def on(self):
        """Returns True if the system is On, else False"""
        return self._system_on

    def off(self):
        """Turns the system off"""
        self._system_on = False
