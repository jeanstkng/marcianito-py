class GameState():
    def __init__(self):
        self.init_state()
        
    def init_state(self):
        self.is_over_asteroid = False
        self.over_asteroid_id = ""
        self.laser_reached = False
        self.player_dir = 0
        self.followers = []
        self.player_health = 2
        self.score = 0