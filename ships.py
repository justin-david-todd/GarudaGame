from lasers import *


class Ship:
    """
    Abstract class for objects piloting through space
    """

    def __init__(self, x, y, laser_array, health=10):
        """
        creates a ship at the x, y coordinate with
        - a ship image
        - a health total
        - a maximum health limit
        - a laser type
        - a collection of lasers fired
        - a laser cool_down_counter
        _ a movement speed
        """
        self._image = {
            # Player Images - image file should be 64x64 pixels
            "main_ship": pygame.image.load("assets/main_ship.png"),

            # Enemy Images - image file should be 32x32 pixels
            # TODO diversify enemy images
            "blue_baddy": pygame.image.load("assets/baddy_1.png"),
            "red_baddy": pygame.image.load("assets/baddy_2.png"),
            "explosion": pygame.image.load("assets/simple_explosion.png"),
            "ArrowBlue": pygame.image.load("assets/ArrowBlue.png"),
            "ArrowGold": pygame.image.load("assets/ArrowGold.png"),
            "ArrowPing": pygame.image.load("assets/ArrowPink.png"),
            "ArrowRed": pygame.image.load("assets/ArrowRed.png"),
            "ArrowStealth": pygame.image.load("assets/ArrowStealth.png"),
            "Block": pygame.image.load("assets/Block.png"),
            "BlueSquid": pygame.image.load("assets/BlueSquid.png"),
            "blueSpark": pygame.image.load("assets/blusSpark.png"),
            "CentiBlue": pygame.image.load("assets/CentiBlue.png"),
            "CentiGreen": pygame.image.load("assets/CentiGreen.png"),
            "CentiheadBlue": pygame.image.load("assets/CentiheadBlue.png"),
            "CentiheadDud": pygame.image.load("assets/CentiheadDud.png"),
            "CentiheadGreen": pygame.image.load("assets/CentiheadGreen.png"),
            "CentiheadPanda": pygame.image.load("assets/CentiheadPanda.png"),
            "CentiheadRed": pygame.image.load("assets/CentiheadRed.png"),
            "FlappyBlue": pygame.image.load("assets/Flappy Blue.png"),
            "FlappyGreen": pygame.image.load("assets/FlappyGreen.png"),
            "FlappyRed": pygame.image.load("assets/FlappyRed.png"),
            "FlappyStealth": pygame.image.load("assets/FlappyStealth.png"),
            "FlappyWhite": pygame.image.load("assets/FlappyWhite.png"),
            "GreenSpark": pygame.image.load("assets/GreenSpark.png"),
            "hammer": pygame.image.load("assets/hammer.png"),
            "metal_1": pygame.image.load("assets/metal_1.png"),
            "MetalSquid": pygame.image.load("assets/MetalSquid.png"),
            "RedMetalSquid": pygame.image.load("assets/RedMetalSquid.png")
        }
        self._x = x
        self._y = y
        self._ship_img = None
        self._mask = None
        self._health = health
        self._max_health = health
        self._laser_type = None
        self._cool_down_counter = 0
        self._speed = 5
        self._lasers = laser_array

        # dimensions of screen ships are flying on.
        self._width = 800
        self._height = 800

    def get_x(self):
        """returns value of ship's x coordinate"""
        return self._x

    def get_y(self):
        """returns value of ship's y coordinate"""
        return self._y

    def get_health(self):
        """returns value of ship's current health"""
        return self._health

    def get_max_health(self):
        """returns value of ship's maximum health"""
        return self._max_health

    def get_speed(self):
        """returns value of ship's speed0"""
        return self._speed

    def get_cool_down_counter(self):
        """returns current value of ship's cool_down_counter"""
        return self._cool_down_counter

    def get_laser_type(self):
        """returns ship's laser type"""
        return self._laser_type

    def get_mask(self):
        """returns the ship's image mask"""
        return self._mask

    def get_width(self):
        """returns width of ship image"""
        return self._ship_img.get_width()

    def get_height(self):
        """returns width of ship image"""
        return self._ship_img.get_height()

    def set_x(self, num):
        """takes a number and sets the x coordinate to that value"""
        self._x = num

    def set_y(self, num):
        """takes a number and sets the y coordinate to that value"""
        self._y = num

    def set_health(self, num):
        """takes a number, sets current health to that number if within max_health"""
        if num <= self._max_health:
            self._health = num

    def set_window(self, width, height):
        """Two pixel values, width and height, and informs ship of window dimensions"""
        self._width = width
        self._height = height

    def recover_health(self, num):
        """
        takes a number and adds it to health value
        if sum is greater than max health, sets it to max health
        """
        self._health += num
        if self._health > self._max_health:
            self._health = self._max_health

    def deplete_health(self, num):
        """takes a number and reduces health by that number"""
        self._health -= num
        if self._health < 0:
            self._health = 0

    def set_laser_type(self, laser_type):
        """
        takes a laser type
        change's ship's laser type to the specified type (string)
        """
        self._laser_type = laser_type

    def horizontal_move(self, num):
        """takes a positive or negative value and adds it to the x coordinate"""
        self._x += num

    def vertical_move(self, num):
        """takes a positive or negative value and adds it to the y coordinate"""
        self._y += num

    def draw(self, surface):
        """
        takes a surface and on that surface
        draws the ship at its current coordinates
        """
        surface.blit(self._ship_img, (self._x, self._y))

    def shoot(self):
        """if the cool_down_counter is zero, fires a laser object from the front of the ship."""
        if self._cool_down_counter <= 0:
            laser = Laser(self._x + self.get_width()/2-8, self._y - 10, self._laser_type)
            self._lasers.append(laser)
            self._cool_down_counter = laser.get_cool_down()

    def cool_down(self):
        if self._cool_down_counter < 0:
            self._cool_down_counter = 0
        elif self._cool_down_counter > 0:
            self._cool_down_counter -= 1

    def collision(self, obj):
        """
        takes an object
        returns True if the ship is colliding with that object, else returns False
        """
        return collide(obj, self)

    # SHIP MOVE PATTERNS
    # TODO diversify movement patterns.
    def move_down(self):
        """movement pattern: sends the enemy down in a straight line"""
        self._y += self._speed


class Player(Ship):
    """
    Ship controlled by the user
    """

    def __init__(self, x, y, laser_array, health):
        super().__init__(x, y,laser_array, health)
        self._ship_img = self._image["main_ship"]
        self._laser_type = "player_green"
        self._mask = pygame.mask.from_surface(self._ship_img)

    def shoot(self):
        """if the cool_down_counter is zero, fires a laser object from the front of the ship."""
        if self._cool_down_counter == 0:
            laser = Laser(self._x + self.get_width()/2-8, self._y - 10, self._laser_type)
            self._lasers.append(laser)
            self._cool_down_counter = laser.get_cool_down()

    def health_bar(self, surface):
        """
        draws two overlapping rectangles, a red one the representing size of max health
        and a green one on top the size of health relative to max health"""
        pygame.draw.rect(surface, (255, 0, 0), (self._x, self._y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(surface, (0, 255, 0), (self._x, self._y + self.get_height() + 10,
                                                self.get_width() * self._health / self._max_health, 10))

    def draw(self, surface):
        super().draw(surface)
        self.health_bar(surface)

    def explode(self):
        """explodes the ship"""
        laser = Laser(self._x - 64 + self.get_width()/2, self._y - 64, "explosion_zero")
        self._lasers.append(laser)


class Enemy(Ship):
    """
    Automated ships attacking the player
    """

    def __init__(self, x, y, laser_array, enemy_type):
        super().__init__(x, y, laser_array)
        # enemy_type : (speed, movement_pattern, ship_img, laser_type, health, point_value)
        species = {
            # TODO diversify enemy types
            "squid": (1, self.move_down, self._image["BlueSquid"], "blueShot", 10, 10)
        }
        self._speed, self._movement_type, self._ship_img = species[enemy_type][0:3]
        self._laser_type, self._health, self._point_value = species[enemy_type][3:6]
        self._mask = pygame.mask.from_surface(self._ship_img)

    def move(self):
        """moves enemy according to movement_type"""
        self._movement_type()

    def explode(self):
        """explodes the ship"""
        laser = Laser(self._x - 64 + self.get_width()/2, self._y - 64, "explosion")
        self._lasers.append(laser)
