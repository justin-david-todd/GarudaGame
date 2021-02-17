# Author: Justin David Todd
# Date: 02/04/2021
# Description: This is a space ship vs aliens shooting game.
# This main function holds the game loop with internal functions for the title screen,
# creating a new game, and updating the window display.
# A ship at the bottom of the screen shoots enemies and scores points based on the number
# of ships defeated.
# The project is still ongoing with a focus on making the ships, player, and lasers
# more modular so their attributes can be easily adapted, adjusted, and generated.
# The current design uses no global variables with all attributes encapsulated in classes and
# aims to use pre-constructed levels rather than merely randomly generating enemies.
import pygame
from Config import Config
from GarudaGame import GarudaGame
import random


def main():
    """
    Loads System configurations.
    Creates the game window opened to title screen
    Current Title Menu options:
        New Game
        Quit
    """
    def new_game():
        """Runs a new game of player ship shooting enemy ships"""
        game = GarudaGame()
        # Configures Game settings to match sys/Config settings.
        game.resize_window(sys.get_width(), sys.get_height())
        # Spawns a new player and loads the sequence of game levels
        player = game.spawn_player()
        game.load_levels()

        # Defines the new game as running, and not lost.
        running = True
        lost = False
        level_starting = False

        # Creates a count for Game Over message duration and creates a clock to track FPS.
        lost_count = 0
        level_count = 0
        clock = pygame.time.Clock()

        def update_window():
            """
            Draws the images to be displayed in each frame, then updates the display.
            Displays GAME OVER at loss
            Controls Player/Enemy/Laser coundaries and actions each frame.
            """
            # Draws Background
            sys.get_window().blit(game.get_background(), (0, 0))

            """Controls Player actions each frame"""
            # Prevents player from moving off-screen
            if player.get_x() < 0:
                player.set_x(0)
            if player.get_x() > game.get_width() - player.get_width():
                player.set_x(game.get_width() - player.get_width())
            if player.get_y() < 0:
                player.set_y(0)
            if player.get_y() > game.get_height() - 20 - player.get_height():
                player.set_y(game.get_height() - 20 - player.get_height())

            # Draws player and decrements player's laser cool down timer each frame
            if not lost:
                player.draw(sys.get_window())
                player.cool_down()

            """ Controls Enemy actions each frame"""
            for enemy in game.get_enemies()[:]:
                enemy.move()
                # controls how often enemies randomly fire
                if random.randrange(0, 3*game.get_fps()) == 1:
                    enemy.shoot()
                enemy.cool_down()
                # enemies disappear when health reaches zero
                if enemy.get_health() <= 0:
                    game.amend_score(enemy.get_value())
                    game.get_enemies().remove(enemy)
                # explodes enemies that reach end of screen or collide with the player
                if enemy.get_y() > game.get_height() - enemy.get_height() or enemy.collision(player):
                    enemy.explode()
                    game.get_enemies().remove(enemy)
                # draws enemy
                enemy.draw(sys.get_window())

            """ Controls Laser Movements each frame."""
            # Moves Player Lasers and removes off-screen lasers
            for laser in game.get_player_lasers()[:]:
                laser.mov()
                # damages enemies hit by player lasers
                for enemy in game.get_enemies()[:]:
                    if laser.collision(enemy):
                        enemy.deplete_health(laser.get_damage())
                        if laser in game.get_player_lasers():
                            game.get_player_lasers().remove(laser)
                if laser.off_screen(game.get_height()):
                    if laser in game.get_player_lasers():
                        game.get_player_lasers().remove(laser)
                laser.draw(sys.get_window())
            # Moves Enemy Lasers and removes off-screen lasers
            for laser in game.get_enemy_lasers()[:]:
                laser.mov()
                # damages player when hit by enemy lasers
                if laser.collision(player):
                    player.deplete_health(laser.get_damage())
                    if laser in game.get_enemy_lasers():
                        game.get_enemy_lasers().remove(laser)
                if laser.off_screen(game.get_height()):
                    if laser in game.get_enemy_lasers():
                        game.get_enemy_lasers().remove(laser)
                laser.draw(sys.get_window())

            # Displays GAME OVER when player loses
            if lost:
                lost_label = sys.font("lost").render("GAME OVER", True, (255, 255, 255))
                temp_width = game.get_width() / 2 - lost_label.get_width() / 2
                sys.get_window().blit(lost_label, (temp_width, game.get_height() / 2 - 50))

            # Displays Level Number at start of new level
            if level_starting:
                if game.get_current_level() < len(game.get_level_sequence()):
                    level_label = sys.font("lost").render("Level " + str(game.get_current_level()), True, (255, 255, 255))
                    temp_width = game.get_width() / 2 - level_label.get_width() / 2
                    sys.get_window().blit(level_label, (temp_width, game.get_height() / 2 - 50))
                elif game.get_current_level() == len(game.get_level_sequence()):
                    level_label = sys.font("lost").render("Welcome to Heck.", True, (255, 255, 255))
                    temp_width = game.get_width() / 2 - level_label.get_width() / 2
                    sys.get_window().blit(level_label, (temp_width, game.get_height() / 2 - 50))
                else:
                    level_label = sys.font("lost").render("So, You Want More???", True, (255, 255, 255))
                    temp_width = game.get_width() / 2 - level_label.get_width() / 2
                    sys.get_window().blit(level_label, (temp_width, game.get_height() / 2 - 50))

            # Displays the current Score in top-left corner
            current_score = sys.font("main").render("Score: " + str(game.get_score()).rjust(7, "0"),
                                                    True, (255, 255, 255))
            sys.get_window().blit(current_score, (10, 10))

            pygame.display.update()

        """Defines Lose conditions, FPS restrictions, Player Controls"""
        # Restricts game speed to config FPS
        while running:
            clock.tick(game.get_fps())

            # Loads next level when are enemies depleted.
            if len(game.get_enemies()) == 0:
                game.next_level()
                level_starting = True
                level_count = 120

            # Defines player lose conditions
            if player.get_health() <= 0:
                if lost_count == 0:
                    player.explode()
                lost = True
                lost_count += 1
            # Displays Game Over for five seconds, then ends game
            if lost_count > game.get_fps() * 5:
                running = False

            # Quits game by clicking close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.off()

            """Defines Player Controls"""
            # Logs keys pressed each frame
            keys = pygame.key.get_pressed()
            # Moves Player by with arrow keys
            if keys[pygame.K_LEFT]:
                player.horizontal_move(-player.get_speed())
            if keys[pygame.K_RIGHT]:
                player.horizontal_move(player.get_speed())
            if keys[pygame.K_UP]:
                player.vertical_move(-player.get_speed())
            if keys[pygame.K_DOWN]:
                player.vertical_move(player.get_speed())

            # Defines keys for Shooting player lasers
            if keys[pygame.K_SPACE]:
                player.shoot()

            # Controls display of new level message.
            if level_count > 0:
                level_count -= 1
                if level_count == 0:
                    level_starting = False

            update_window()

    def title_screen():
        """Runs the title screen menu."""
        display_title = True
        # Defines Menu Screen options
        menu_options = ["new game", "quit"]
        select_option = 0

        sys.display_decor()

        while display_title:
            # Defines contents displayed on Title Screen
            game_title = sys.font("title").render("Garuda", True, (255, 255, 100))
            game_title2 = sys.font("sub menu").render("New Game", True, (255, 255, 255))
            game_title3 = sys.font("sub menu").render("Quit", True, (255, 255, 255))
            game_title4 = sys.font("sub title").render("SpaceBar to Shoot. Arrow Keys to Move.", True, (255, 255, 255))
            game_title5 = sys.font("sub title").render("Created by Justin David Todd", True, (255, 255, 255))
            cursor = sys.get_image("main_ship")
            cursor_position = sys.get_height()*3//4 - sys.get_height()//10 + select_option*sys.get_height()//8

            # Draws Title Screen and Menu
            sys.get_window().blit(sys.get_background(), (0, 0))
            sys.get_window().blit(game_title, (sys.get_width() // 2 - game_title.get_width() // 2,
                                               sys.get_height()//3))
            sys.get_window().blit(game_title2, (sys.get_width() // 2 - game_title2.get_width() // 2,
                                                sys.get_height()*3//4 - sys.get_height()//10))
            sys.get_window().blit(game_title3, (sys.get_width() // 2 - game_title2.get_width() // 2,
                                                sys.get_height() * 3 // 4))
            sys.get_window().blit(game_title4, (sys.get_width() // 2 - game_title4.get_width() // 2,
                                                sys.get_height()-100))
            sys.get_window().blit(game_title5, (sys.get_width() // 2 - game_title5.get_width() // 2,
                                                20))
            sys.get_window().blit(cursor, (sys.get_width()//2 - game_title2.get_width()*11//14,
                                           cursor_position))
            pygame.display.update()

            """Title Menu Controls"""
            for event in pygame.event.get():
                # Quits game by clicking close button
                if event.type == pygame.QUIT:
                    display_title = False
                    sys.off()
                # Navigates Menu with UP/LEFT and DOWN/RIGHT keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        select_option -= 1
                        if select_option < 0:
                            select_option = len(menu_options) - 1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        select_option += 1
                        if select_option >= len(menu_options):
                            select_option = 0
                    # Select menu option with SPACE/RETURN/ENTER
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
                        display_title = False
                        sys.set_destination(menu_options[select_option])
                        if sys.get_destination() == "quit":
                            sys.off()
    """
    Creates the game's Config in an "on" state.
    Defaults to title_screen on start or when a new_game ends.
    System turns off and program exits if window is closed or "QUIT" is selected from title_screen. 
    """
    sys = Config()
    while sys.on():
        title_screen()
        if sys.on() and sys.get_destination() == "new game":
            new_game()


if __name__ == "__main__":
    main()
