# Author: Justin David Todd
# Last Modified: 02/04/2021
# Description: Defines collisions, designs the laser objects to be fired by the ships
#   including a dictionary of all the laser varieties and explosions.

import pygame


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
        # Dictionary of Laser Images
        self._image = {
            # Laser Images = image file should be 16 x 32 pixels
            "green_blast": pygame.image.load("assets/green_blast.png"),
            "blank": pygame.image.load("assets/Blank.png"),
            "explosion": pygame.image.load("assets/simple_explosion.png"),
            "green_laser": pygame.image.load("assets/laser_green.png"),
            "lightning": pygame.image.load("assets/lightning blue.png"),
            "blueShot": pygame.image.load("assets/pellet blue.png"),
            "greenShot": pygame.image.load("assets/pellet green.png"),
            "redShot": pygame.image.load("assets/pellet red.png"),
            "yellowShot": pygame.image.load("assets/pellet yellow.png"),
            "rayBlue": pygame.image.load("assets/rayBlue.png"),
            "rayGreen": pygame.image.load("assets/rayGreen.png"),
            "rayRed": pygame.image.load("assets/rayRed.png"),
            "blasterGreen": pygame.image.load("assets/blasterGreen.png"),
            "blasterRed": pygame.image.load("assets/blasterRed.png")
        }

        # Dictionary of Laser Types
        self._laser_type = {
            # "laser_type" : (damage, velocity, cool_down, laser_img, move_pattern)
            "green": (10, 10, 15, self._image["green_laser"], self.normal),
            "player_green": (100, -10, 15, self._image["green_blast"], self.normal),
            "explosion": (30, 10, 15, self._image["explosion"], self.delayed),
            "explosion_zero": (0, 10, 15, self._image["explosion"], self.delayed),
            "lightning": (30, 30, 5, self._image["lightning"], self.normal),
            "blueShot": (10, 10, 15, self._image["blueShot"], self.normal),
            "greenShot": (10, 10, 15, self._image["greenShot"], self.normal),
            "redShot": (10, 10, 15, self._image["redShot"], self.normal),
            "yellowShot": (10, 10, 15, self._image["yellowShot"], self.normal),
            "rayBlue": (30, 10, 15, self._image["rayBlue"], self.normal),
            "rayGreen": (10, 10, 15, self._image["rayGreen"], self.normal),
            "rayRed": (20, 10, 15, self._image["rayRed"], self.normal),
            "blasterGreen": (10, 10, 15, self._image["blasterGreen"], self.weave),
            "blasterGreen2": (10, 10, 15, self._image["blasterGreen"], self.weave2),
            "blasterRed": (10, 10, 15, self._image["blasterRed"], self.normal),
            "blank": (0, 1000, 1000, self._image["blank"], self.normal)

        }
        self._x = x
        self._y = y

        # Counter and direction marker for timing movement pattern maneuvers
        self._move_timer = 0
        self._direction = 0

        # Define Laser Attributes based on type
        self._damage = self._laser_type[laser_type][0]         # Damage
        self._velocity = self._laser_type[laser_type][1]       # Velocity
        self._cool_down = self._laser_type[laser_type][2]      # Cool Down Time
        self._laser_img = self._laser_type[laser_type][3]      # Image
        self.move_pattern = self._laser_type[laser_type][4]     # Movement Pattern

        # Define Mask for collisions
        self._mask = pygame.mask.from_surface(self._laser_img)

    # Get Methods
    def get_x(self):
        """returns laser's x coordinate"""
        return self._x

    def get_y(self):
        """returns laser's y coordinate"""
        return self._y

    def get_width(self):
        """returns width of laser's image"""
        return self._laser_img.get_width()

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

    # Other Methods
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
        return not (height >= self._y > 1)

    def collision(self, obj):
        """
        takes an object
        returns True if the laser is colliding with that object, else returns False
        """
        return collide(obj, self)

    def horizontal_move(self, num):
        """takes a positive or negative value and adds it to the x coordinate"""
        self._x += num

    def vertical_move(self, num):
        """takes a positive or negative value and adds it to the y coordinate"""
        self._y += num

    # Collection of Laser Movement Patterns
    def normal(self):
        """shoots laser in straight line"""
        self._y += self._velocity

    def weave(self):
        """shoots laser in straight line"""
        if self._move_timer < 30:
            self._x += 3
        else:
            self._x -= 3
        self._move_timer += 1
        if self._move_timer > 60:
            self._move_timer = 0
        self._y += self._velocity

    def weave2(self):
        """shoots laser in straight line"""
        if self._move_timer < 30:
            self._x -= 3
        else:
            self._x += 3
        self._move_timer += 1
        if self._move_timer > 60:
            self._move_timer = 0
        self._y += self._velocity

    def delayed(self):
        """holds blast in place for .5 seconds, then moves below the screen (disappears)"""
        if self._move_timer < 30:
            self._move_timer += 1
        else:
            self._y = 10000
