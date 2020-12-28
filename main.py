# Author: Justin David Todd
# Date: 12/21/2020
# Description: This is a mock version of the game Phoenix I loved playing as a kid
# where a ship at the bottom of the screen shoots enemies and scores points based on the number
# of ships defeated, using points to buy upgrades.
# The current version looks more like Space Invaders with power ups
# but the project is still ongoing with a focus on making the ships, player, and lasers
# more modular so their attributes can be more easily adapted, adjusted, and generated.
# The current design also aims to use pre-constructed levels instead of simply
# randomly generated enemies.

import pygame
import random
pygame.font.init()

# General Display Attributes
# edit: potentially add encompassing PhoenixGame class to hold game settings, images, 2
# and player/enemy/laser lists, permitting division of objects into multiple .py files for modularization.
WIDTH = 800
HEIGHT = 800
FPS = 60

# Background, Caption, and Icon Images
BG_1 = pygame.transform.scale(pygame.image.load("assets/starlight_bg.png"), (WIDTH, HEIGHT))

# Sprites
# Player Images - image file should be 64x64 pixels
MAIN_SHIP = pygame.image.load("assets/main_ship.png")

# Laser Images - image file should be 16x32 pixels
GREEN_LASER = pygame.image.load("assets/laser_green.png")
GREEN_BLAST = pygame.image.load("assets/green_blast.png")
EXPLOSION = pygame.image.load("assets/simple_explosion.png")

# Enemy Images - image file should be 32x32 pixels
BLUE_BADDY = pygame.image.load("assets/baddy_1.png")
RED_BADDY = pygame.image.load("assets/baddy_2.png")

# Game Fonts
main_font = pygame.font.SysFont('comicsansms', 50)
lost_font = pygame.font.SysFont('comicsansms', 80)

# Window Attributes
background = BG_1
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(BLUE_BADDY)
pygame.display.set_caption("PHOENIX prototype")

# Object Lists
# Lists of all existing objects in the game for iteration by type
enemy_array = []
enemy_lasers = []
player_lasers = []


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
        self._laser_type = {
            # "laser_type" : (damage, velocity, cool_down, laser_img, move_pattern)
            "green": (10, 10, 15, GREEN_LASER, self.normal),
            "player_green": (10, -10, 15, GREEN_BLAST, self.normal),
            "explosion": (30, 10, 15, EXPLOSION, self.delayed),
            "explosion_zero": (0, 10, 15, EXPLOSION, self.delayed)
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
            self._y = HEIGHT + 1


class Ship:
    """
    Abstract class for objects piloting through space
    """

    def __init__(self, x, y, health=10):
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
        self._x = x
        self._y = y
        self._ship_img = None
        self._mask = None
        self._health = health
        self._max_health = health
        self._laser_type = None
        self._cool_down_counter = 0
        self._speed = 5

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
            enemy_lasers.append(laser)
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
    def move_down(self):
        """movement pattern: sends the enemy down in a straight line"""
        self._y += self._speed


class Player(Ship):
    """
    Ship controlled by the user
    """

    def __init__(self, x, y, health):
        super().__init__(x, y, health)
        self._ship_img = MAIN_SHIP
        self._laser_type = "player_green"
        self._mask = pygame.mask.from_surface(self._ship_img)

    def shoot(self):
        """if the cool_down_counter is zero, fires a laser object from the front of the ship."""
        if self._cool_down_counter == 0:
            laser = Laser(self._x + self.get_width()/2-8, self._y - 10, self._laser_type)
            player_lasers.append(laser)
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
        player_lasers.append(laser)


class Enemy(Ship):
    """
    Automated ships attacking the player
    """

    def __init__(self, x, y, enemy_type):
        super().__init__(x, y)
        # enemy_type : (speed, movement_type, ship_img, laser_type, health, point_value)
        species = {
            "squid": (1, self.move_down, BLUE_BADDY, "green", 10, 10)
        }
        self._speed, self._movement_type, self._ship_img = species[enemy_type][0:3]
        self._laser_type, self._health, self._point_value = species[enemy_type][3:6]
        self._mask = pygame.mask.from_surface(self._ship_img)
        self._explosion_img = EXPLOSION

    def move(self):
        """moves enemy according to movement_type"""
        self._movement_type()

    def explode(self):
        """explodes the ship"""
        laser = Laser(self._x - 64 + self.get_width()/2, self._y - 64, "explosion")
        enemy_lasers.append(laser)


def level_one():
    """spawns enemies for level 1"""
    # WAVE 1
    left_indent = 64
    spacing = 64
    start_distance = 100
    num_enemies = 10
    enemy_type = "squid"
    for spawn in range(0, num_enemies):
        enemy = Enemy(left_indent + spacing * spawn, start_distance, enemy_type)
        enemy_array.append(enemy)

    start_distance = 164

    for spawn in range(0, num_enemies):
        enemy = Enemy(left_indent + spacing * spawn, start_distance, enemy_type)
        enemy_array.append(enemy)


def main():
    """defines user interface features for the game and contains the game loop"""
    running = True
    lost = False
    lost_count = 0
    clock = pygame.time.Clock()

    # creates player ship at the center bottom of the screen.
    player = Player(0, 0, 100)
    player.set_x(WIDTH / 2 - player.get_width() / 2)
    player.set_y(HEIGHT - 100)

    def update_window():
        """
        Draws the images to be displayed in each frame, then updates the display.
        Drawings occur in the following order:
        draws the background
        updates the display
        """
        WIN.blit(background, (0, 0))

        if lost:
            lost_label = lost_font.render("GAME OVER", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - 50))

        # prevents player from moving off-screen
        if player.get_x() < 0:
            player.set_x(0)
        if player.get_x() > WIDTH - player.get_width():
            player.set_x(WIDTH - player.get_width())
        if player.get_y() < 0:
            player.set_y(0)
        if player.get_y() > HEIGHT - 20 - player.get_height():
            player.set_y(HEIGHT - 20 - player.get_height())

        # draws player and decrements player's laser cool down timer
        if not lost:
            player.draw(WIN)
            player.cool_down()

        for enemy in enemy_array[:]:
            enemy.move()
            # controls how often enemies randomly fire
            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()
            enemy.cool_down()
            # enemies disappear when health reaches zero
            if enemy.get_health() <= 0:
                enemy_array.remove(enemy)
            # explodes enemies that reach end of screen or collide with the player
            if enemy.get_y() > HEIGHT - enemy.get_height() or enemy.collision(player):
                enemy.explode()
                enemy_array.remove(enemy)
            # draws enemy
            enemy.draw(WIN)

        # moves player lasers and removes off-screen lasers
        for laser in player_lasers[:]:
            laser.mov()
            # damages enemies hit by player lasers
            for enemy in enemy_array[:]:
                if laser.collision(enemy):
                    enemy.deplete_health(laser.get_damage())
                    if laser in player_lasers:
                        player_lasers.remove(laser)
            if laser.off_screen(HEIGHT):
                if laser in player_lasers:
                    player_lasers.remove(laser)
            laser.draw(WIN)
        # moves enemy lasers and removes off-screen lasers
        for laser in enemy_lasers[:]:
            laser.mov()
            # damages player when hit by enemy lasers
            if laser.collision(player):
                player.deplete_health(laser.get_damage())
                if laser in enemy_lasers:
                    enemy_lasers.remove(laser)
            if laser.off_screen(HEIGHT):
                if laser in enemy_lasers:
                    enemy_lasers.remove(laser)
            laser.draw(WIN)
        pygame.display.update()

    # spawns level one enemies
    level_one()

    while running:
        clock.tick(FPS)

        # player lose conditions
        if player.get_health() <= 0:
            if lost_count == 0:
                player.explode()
            lost = True
            lost_count += 1
        if lost_count > FPS * 5:           # displays "lose" message for five seconds, then ends game
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows quitting game by clicking close button
                running = False

        keys = pygame.key.get_pressed()
        # defines player movement with arrow keys
        if keys[pygame.K_LEFT]:
            player.horizontal_move(-player.get_speed())
        if keys[pygame.K_RIGHT]:
            player.horizontal_move(player.get_speed())
        if keys[pygame.K_UP]:
            player.vertical_move(-player.get_speed())
        if keys[pygame.K_DOWN]:
            player.vertical_move(player.get_speed())
        # defines key for shooting player lasers
        if keys[pygame.K_SPACE]:
            player.shoot()

        update_window()


main()
