import os, random, uuid
import pygame
from pygame import Vector2
from laser_beam import LaserBeam

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game_state):
        super().__init__()

        self.id = uuid.uuid4()
        self.image = pygame.image.load(os.path.join('images','enemy.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice([random.randint(-1280, 0), random.randint(1280, 1280 * 2)]), random.randint(0, 720))
        self.position = self.rect.center
        self.game_state = game_state
        self.is_alive = True
        self.direction = Vector2(random.choice([-1, 1]), 0)
        self.speed = 0.05
        self.laser_beam = LaserBeam(self.rect.center, self.game_state, (200,100,10), True, self.id)
        self.laser_reached = False
        
        self.dt = 0
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self, dt):
        self.dt = dt

        if self.position[0] >= 3600:
            self.direction = Vector2(-1, 0)
        elif self.position[0] <= -3600:
            self.direction = Vector2(1, 0)

        temp_direction = Vector2(self.direction.x, 0)
        if self.game_state.player_dir == -1:
            temp_direction.x = -1
        elif self.game_state.player_dir == 1:
            temp_direction.x = 1
        else:
            temp_direction.x = self.direction.x

        self.position += temp_direction * self.speed * dt
        self.rect.center = self.position
        
        
    