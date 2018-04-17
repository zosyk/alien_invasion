import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load("images/alien.png")
        self.image = pygame.transform.scale(self.image, (settings.alien_width, settings.alien_height))
        self.rect = self.image.get_rect()

        # Start each new alien near the top of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Move the alien right or left"""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """ Return True if alien is at adge of screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

        return False