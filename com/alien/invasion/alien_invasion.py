import sys
import pygame
import game_functions as gf
from pygame.locals import *

from settings import Settings
from ship import Ship

from pygame.sprite import Group


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(settings, screen)
    # make a group to store bullets in
    bullets = Group()


    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        bullets.update()

        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        gf.update_screen(settings, screen, ship, bullets)


run_game()
