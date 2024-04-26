class GameState():
    def __init__(self):
        self.is_over_asteroid = False
        self.over_asteroid_id = ""
        self.laser_reached = False
        self.player_dir = 0
        self.followers = []