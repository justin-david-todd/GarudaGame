# Author: Justin David Todd
# Last Modified: 01/31/2021
# Description: Defines collisions, designs the laser objects to be fired by the ships
#   including a dictionary of all the laser varieties and explosions.

import pygame
import random
pygame.font.init()


def collide(obj1, obj2):
    """
    Takes two objects with masks and x/y coordinates.
    Compares the masks of the two objects;
    returns True if they have overlap, else returns False.
    """
    offset_x = obj2.get_x() - obj1.get_x()
    offset_y = obj2.get_y() - obj1.get_y()
    return obj1.get_mask().overlap(obj2.get_mask(), (int(offset_x), int(offset_y))) is not None


class Laser:
    """
    A laser object to be fired by both player and enemy ships.
    Cause damage and disappear upon impact.
    """

    def __init__(self, x, y, laser_type):
        """
        takes a starting x and y coordinates and a laser image
        creates a laser object that propels at a set speed until colliding with the end of the screen
        or an opposing ship.
        """
        # dictionary of predefined laser types and their attributes
        self._image = {
            # Laser Images = image file should be 16 x 32 pixels
            "green_blast": pygame.image.load("assets/green_blast.png"),
            "explosion": pygame.image.load("assets/simple_explosion.png"),
            "green_laser": pygame.image.load("assets/laser_green.png")
        }
        self._laser_type = {
            # "laser_type" : (damage, velocity, cool_down, laser_img, move_pattern)
            "green": (10, 10, 15, self._image["green_laser"], self.normal),
            "player_green": (10, -10, 15, self._image["green_blast"], self.normal),
            "explosion": (30, 10, 15, self._image["explosion"], self.delayed),
            "explosion_zero": (0, 10, 15, self._image["explosion"], self.delayed)
        }

        self._x = x
        self._y = y
        self._damage, self._velocity, self._cool_down, self._laser_img, \
            self.move_pattern = self._laser_type[laser_type]
        self._mask = pygame.mask.from_surface(self._laser_img)
        self._move_timer = 0

    def get_x(self):
        """returns laser's x coordinate"""
        return self._x

    def get_y(self):
        """returns laser's y coordinate"""
        return self._y

    def get_damage(self):
        """returns laser's damage value"""
        return self._damage

    def get_velocity(self):
        """returns laser's rate of travel"""
        return self._velocity

    def get_cool_down(self):
        """returns laser's cool_down length"""
        return self._cool_down

    def get_mask(self):
        """returns the laser's image mask"""
        return self._mask

    def get_move_timer(self):
        """returns the laser's move_timer"""
        return self._move_timer

    def horizontal_move(self, num):
        """takes a positive or negative value and adds it to the x coordinate"""
        self._x += num

    def vertical_move(self, num):
        """takes a positive or negative value and adds it to the y coordinate"""
        self._y += num

    def draw(self, surface):
        """
        takes a surface
        draws the laser at its current coordinates on that surface
        """
        surface.blit(self._laser_img, (self._x, self._y))

    def mov(self):
        """moves the laser according to its movement pattern once fired"""
        self.move_pattern()

    def off_screen(self, height):
        """
        takes the height of the screen in pixels
        returns True if the laser in off-screen, else returns False
        """
        return not (height >= self._y >= 0)

    def collision(self, obj):
        """
        takes an object
        returns True if the laser is colliding with that object, else returns False
        """
        return collide(obj, self)

    # LASER MOVE PATTERNS

    def normal(self):
        """shoots laser in straight line"""
        self._y += self._velocity

    def delayed(self):
        """holds blast in place for .5 seconds, then moves below the screen (disappears)"""
        if self._move_timer < 30:
            self._move_timer += 1
        else:
            self._y = 10000
