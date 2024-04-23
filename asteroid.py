import os
import pygame
import random, uuid
from pygame import Vector2

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game_state):
        super().__init__()
        # Explosion
        self.sprite_sheet = pygame.image.load(os.path.join('images','explotion.png'))
        self.frame_width = 256
        self.frames_per_row = 8
        self.total_frames = 8
        self.rows, self.cols = self.calculate_layout()
        self.current_frame = 0
        self.explotion_image = self.get_current_frame()
        self.explotion_image = pygame.transform.scale(self.explotion_image, (100, 100))
        self.time_passed = 0
        self.explosion_started = False

        # Asteroid
        self.id = uuid.uuid4()
        self.image = pygame.image.load(os.path.join('images','asteroid.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 1280), random.randint(0, 720))
        self.position = self.rect.center
        self.game_state = game_state
        self.health = 100
        self.is_alive = True
        self.color_rate = 0.005
        self.direction = Vector2(random.choice([-1, 1]), 0)
        self.speed = 0.075
        
        self.dt = 0
        
    def animate(self):
        if self.current_frame < 8 and self.time_passed >= 50:
            self.time_passed = 0
            self.current_frame = (self.current_frame + 1)
            self.image = self.get_current_frame()
            self.image = pygame.transform.scale(self.image, (100, 100))
            if self.current_frame == 8:
                self.is_alive = False
                self.kill()
        else:
            self.time_passed += self.dt
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self, dt):
        self.dt = dt
        if self.explosion_started:
            self.animate()

        if self.health <= 0:
            self.game_state.over_asteroid_id = ""
            self.game_state.is_over_asteroid = False
            if not self.explosion_started:
                self.image = self.explotion_image
            self.explosion_started = True
            return
        
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
        
        is_over_asteroid = self.rect.collidepoint(pygame.mouse.get_pos())
                
        if is_over_asteroid:
            self.game_state.over_asteroid_id = self.id
            self.game_state.is_over_asteroid = True
            if self.game_state.laser_reached:
                self.health -= 1
                self.image = self.create_image_surface_with_fog(self.image, (255, 0, 0), self.color_rate)
        elif self.game_state.over_asteroid_id == self.id and not is_over_asteroid:
            self.game_state.over_asteroid_id = ""
            self.game_state.is_over_asteroid = False
    
    def create_image_surface_with_fog(self, img, fog_color, fog_rate):
        _,_,width,height = img.get_rect()
        fog_color = [color * fog_rate for color in fog_color]

        new_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        new_surface.blit(img, img.get_rect())
        new_surface.fill((255, 0, 0, self.color_rate), img.get_rect(), special_flags=pygame.BLEND_MULT)
        new_surface.fill(fog_color, img.get_rect(), special_flags=pygame.BLEND_RGB_ADD)
        return new_surface
    
    def get_current_frame(self):
        row = self.current_frame // self.frames_per_row
        col = self.current_frame % self.frames_per_row if row < self.rows - 1 else self.current_frame % self.cols
        frame_rect = pygame.Rect(col * self.frame_width, row * self.frame_width, self.frame_width, self.frame_width)
        frame_image = pygame.Surface((self.frame_width, self.frame_width), pygame.SRCALPHA)
        frame_image.blit(self.sprite_sheet, (0, 0), frame_rect)
        return frame_image
    
    def calculate_layout(self):
        rows = self.total_frames // self.frames_per_row
        cols = self.frames_per_row
        if self.total_frames % self.frames_per_row != 0:
            rows += 1
            cols = self.total_frames % self.frames_per_row
        return rows, cols
    
    