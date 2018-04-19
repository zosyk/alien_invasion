import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()

        self.screen = screen
        self.settings = settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png')
        self.image = pygame.transform.scale(self.image, (settings.ship_width, settings.ship_height))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        # movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.settings.ship_speed_factor

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx