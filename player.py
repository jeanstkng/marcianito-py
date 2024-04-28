import pygame
from constants import game_constants
from marcianito import Marcianito

class Player(Marcianito):
    health_capacity = 100
    current_health = 0
    
    def update(self, movement):
        self.rect.move_ip(movement.x, movement.y)
        
        self.rect.left = max(350, min(self.rect.left, self.screen_width - 450))
        self.rect.top = max(0, min(self.rect.top, self.screen_height - self.rect.height))
        
        self.current_health = self.game_state.player_health