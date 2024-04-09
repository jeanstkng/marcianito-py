import os

import pygame
from pygame.locals import *
from pygame.math import Vector2
from player import Player
from constants import game_constants
from background import Background

os.environ["SLD_VIDEO_CENTERED"] = "1"

class Game():
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        
        self.window = pygame.display.set_mode((game_constants.get("window_width"),
                                               game_constants.get("window_height")))
        self.bg = Background(self.window)
        sprite_sheet = pygame.image.load(os.path.join('images','marcianito.png'))

        self.player = Player(sprite_sheet)
        self.all_sprites = pygame.sprite.Group(self.player)
        
        pygame.display.set_caption("Marcianito 100% Real")
        self.running = True
        self.movement = pygame.Vector2(0,0)

    def processInput(self):
        self.movement = Vector2(0,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        elif keys[pygame.K_d]:
            self.movement.x = 8
        elif keys[pygame.K_a]:
            self.movement.x = -8
        elif keys[pygame.K_s]:
            self.movement.y = 8
        elif keys[pygame.K_w]:
            self.movement.y = -8
    
    def update(self):
        self.all_sprites.update(self.movement)
        self.bg.update(self.player.rect)

    def render(self):
        self.window.fill((0,0,0))
        
        self.bg.draw()
        self.player.animate()
        self.all_sprites.draw(self.window)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


game = Game()
game.run()
pygame.quit()