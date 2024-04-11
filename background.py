import pygame
import os

class Background():
    def __init__(self, window):
        super().__init__()
        self.bg = pygame.image.load(os.path.join('images','bg.png')).convert()
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = -self.bg.get_width()
        self.speed = 0.8
        self.window = window
        
    def update(self, rect):
        if rect.x >= 800:
            self.moveBackgrounds(-1)
        elif rect.x <= 350:
            self.moveBackgrounds(1)

        if self.bgX < self.bg.get_width() * -1:
            self.bgX = self.bg.get_width()
        
        if self.bgX2 < self.bg.get_width() * -1:
            self.bgX2 = self.bg.get_width()
            
        if self.bgX3 > self.bg.get_width() * 2:
            self.bgX3 = -self.bg.get_width()

    def draw(self):
        self.window.blit(self.bg, (self.bgX, 0))
        self.window.blit(self.bg, (self.bgX2, 0))
        self.window.blit(self.bg, (self.bgX3, 0))
        
    def moveBackgrounds(self, multiplier):
        self.bgX += self.speed * multiplier
        self.bgX2 += self.speed * multiplier
        self.bgX3 += self.speed * multiplier