class GameStats():
    """ Track statistics for alien invasion"""

    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """ Initialize statistics that can change during the game """
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1
