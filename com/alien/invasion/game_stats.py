class GameStats():
    """ Track statistics for alien invasion"""

    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = True

    def reset_stats(self):
        """ Initialize statistics that can change during the game """
        self.ships_left = self.settings.ships_limit
