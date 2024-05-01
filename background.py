import pygame
import os

class Background():
    def __init__(self, window, game_state):
        super().__init__()
        self.bg = pygame.image.load(os.path.join('data','images','bg.png')).convert()
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = -self.bg.get_width()
        self.bg_width = self.bg.get_width()
        self.speed = 2
        self.window = window
        self.game_state = game_state
        
    def update(self, player_rect):
        if player_rect.x >= 700:
            self.moveBackgrounds(-1)
            self.game_state.player_dir = -1
        elif player_rect.x <= 580:
            self.moveBackgrounds(1)
            self.game_state.player_dir = 1
        else:
            self.game_state.player_dir = 0

        if self.bgX <= -self.bg_width or self.bgX >= self.bg_width:
            self.bgX = 0
        
        if self.bgX2 <= 0 or self.bgX2 >= self.bg_width * 2:
            self.bgX2 = self.bg_width
        
        if self.bgX3 <= self.bg_width * -2 or self.bgX3 >= 0:
            self.bgX3 = -self.bg_width

    def draw(self):
        self.window.blit(self.bg, (self.bgX, 0))
        self.window.blit(self.bg, (self.bgX2, 0))
        self.window.blit(self.bg, (self.bgX3, 0))
        
    def moveBackgrounds(self, multiplier):
        self.bgX += self.speed * multiplier
        self.bgX2 += self.speed * multiplier
        self.bgX3 += self.speed * multiplier