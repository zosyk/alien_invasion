import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():

    def __init__(self, settings, screen, stats):
        """ Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """ Show how many ships are left"""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        """ Turn the score into a rendered image"""
        score_str = self.stats.score
        score_str = "{:,}".format(score_str)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        score_str = self.stats.high_score
        score_str = "{:,}".format(score_str)
        self.high_score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = 20

    def prep_level(self):
        """Turn the level into a rendered image."""

        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.settings.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """ Draw score to the screen """

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.ships.draw(self.screen)

