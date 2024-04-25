import pygame
from constants import game_constants
from marcianito import Marcianito

class Player(Marcianito):
    def update(self, movement):
        self.rect.move_ip(movement.x, movement.y)
        
        self.rect.left = max(350, min(self.rect.left, self.screen_width - 450))
        self.rect.top = max(0, min(self.rect.top, self.screen_height - self.rect.height))