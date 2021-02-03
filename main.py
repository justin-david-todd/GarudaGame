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

from GarudaGame import *


def main():
    """defines user interface features for the game and contains the game loop"""
    game = GarudaGame()
    player = game.spawn_player()
    game.load_levels()

    running = True
    lost = False
    lost_count = 0
    clock = pygame.time.Clock()

    def update_window():
        """
        Draws the images to be displayed in each frame, then updates the display.
        Drawings occur in the following order:
        draws the background
        updates the display
        """
        game.get_window().blit(game.get_background(), (0, 0))

        if lost:
            lost_label = game.font("lost").render("GAME OVER", True, (255, 255, 255))
            game.get_window().blit(lost_label,
                                   (game.get_width()/2 - lost_label.get_width()/2, game.get_height()/2 - 50))

        # prevents player from moving off-screen
        if player.get_x() < 0:
            player.set_x(0)
        if player.get_x() > game.get_width() - player.get_width():
            player.set_x(game.get_width() - player.get_width())
        if player.get_y() < 0:
            player.set_y(0)
        if player.get_y() > game.get_height() - 20 - player.get_height():
            player.set_y(game.get_height() - 20 - player.get_height())

        # draws player and decrements player's laser cool down timer
        if not lost:
            player.draw(game.get_window())
            player.cool_down()

        for enemy in game.get_enemies()[:]:
            enemy.move()
            # controls how often enemies randomly fire
            if random.randrange(0, 3*game.get_fps()) == 1:
                enemy.shoot()
            enemy.cool_down()
            # enemies disappear when health reaches zero
            if enemy.get_health() <= 0:
                game.get_enemies().remove(enemy)
            # explodes enemies that reach end of screen or collide with the player
            if enemy.get_y() > game.get_height() - enemy.get_height() or enemy.collision(player):
                enemy.explode()
                game.get_enemies().remove(enemy)
            # draws enemy
            enemy.draw(game.get_window())

        # moves player lasers and removes off-screen lasers
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
            laser.draw(game.get_window())
        # moves enemy lasers and removes off-screen lasers
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
            laser.draw(game.get_window())
        pygame.display.update()

    while running:
        clock.tick(game.get_fps())

        # begins next level if enemies depleted.
        if len(game.get_enemies()) == 0:
            game.next_level()

        # player lose conditions
        if player.get_health() <= 0:
            if lost_count == 0:
                player.explode()
            lost = True
            lost_count += 1
        if lost_count > game.get_fps() * 5:           # displays "lose" message for five seconds, then ends game
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
