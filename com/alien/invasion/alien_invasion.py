import game_functions as gf
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(settings, screen)
    # make a group to store bullets in
    bullets = Group()
    aliens = Group()
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)
    play_button = Button(settings, screen, "Play")


    gf.create_fleet(aliens, settings, screen)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, stats, screen, ship, aliens, bullets, play_button, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, aliens, bullets, stats, sb)
            gf.update_aliens(settings, stats, screen, ship, aliens, bullets, sb)

        gf.update_screen(settings, stats, sb, screen, ship, aliens, bullets, play_button)


run_game()
