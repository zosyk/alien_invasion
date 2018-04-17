import game_functions as gf
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship


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

    gf.create_fleet(aliens, settings, screen)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(settings, aliens)
        gf.update_screen(settings, screen, ship, aliens, bullets)


run_game()
