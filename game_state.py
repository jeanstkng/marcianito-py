class GameState():
    def __init__(self):
        self.init_state()
        
    def init_state(self):
        self.is_over_asteroid = False
        self.over_asteroid_id = ""
        self.laser_reached = False
        self.player_dir = 0
        self.followers = []
        self.player_health = 30
        self.score = 0
        self.enemy_lasers_reached = []
        self.laser_attack_increment = 0