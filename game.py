import os

import pygame
from pygame.locals import *
from pygame.math import Vector2
from player import Player
from constants import game_constants
from background import Background
from laser_beam import LaserBeam
from asteroid import Asteroid
from game_state import GameState

os.environ["SLD_VIDEO_CENTERED"] = "1"

screen_size = Vector2(game_constants.get("window_width"), game_constants.get("window_height"))
screen_center = screen_size // 2
class Game():
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        
        self.surface = pygame.display.set_mode((game_constants.get("window_width"),
                                               game_constants.get("window_height")))
        self.bg = Background(self.surface)
        sprite_sheet = pygame.image.load(os.path.join('images','marcianito.png'))

        self.player = Player(sprite_sheet)
        
        self.targets = [Asteroid(self.game_state),Asteroid(self.game_state),
                        Asteroid(self.game_state),Asteroid(self.game_state),
                        Asteroid(self.game_state)]
        
        self.all_sprites = pygame.sprite.Group(self.player, self.targets)
        self.laser_beam = LaserBeam(self.player.rect.center, self.game_state)
        
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
        self.player.update(self.movement)
        self.laser_beam.update(self.player.rect.center)
        self.bg.update(self.player.rect)
        for target in self.targets:
            target.update()

    def render(self):
        self.surface.fill((0,0,0))
        
        self.bg.draw()
        self.laser_beam.draw(self.surface)
        for target in self.targets:
            target.draw(self.surface)
                    
        self.player.animate()
        self.all_sprites.draw(self.surface)
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