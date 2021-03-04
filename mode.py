class Mode:

    def __init__(self, mode_name):
        self.name = mode_name
        self.num_games = 0
        self.total_time = 0
    
    def __str__(self):
        return '{:<16s}{:>8d}{:>12d}'.format(self.name, self.num_games, self.total_time)
    
    def update(self, match):
        self.num_games += 1
        self.total_time += match['gameDuration']