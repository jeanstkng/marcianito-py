import os
from constants import game_constants
import pygame
from pygame import Vector2
import math

screen_center_x = game_constants.get("window_width") / 2

class LaserBeam():
    def __init__(self, pivot):
        self.x_scale = 10
        self.x_pos_increment = 5
        self.laser = pygame.image.load(os.path.join('images','laser.png')).convert_alpha()
        self.pivot = pivot
        self.pos = Vector2(pivot) + (self.x_pos_increment, 0)    
        self.mouse_pos = Vector2(pygame.mouse.get_pos())
        
        self.handle_image_change_by_mouse_pos(self.pivot, self.mouse_pos)
        
        self.rect = self.image.get_rect(center = self.pos)
        

    def update(self, pivot):
        self.mouse_pos = Vector2(pygame.mouse.get_pos())
        
        self.handle_image_change_by_mouse_pos(pivot, self.mouse_pos)
        
        if self.mouse_pos.x < screen_center_x:
            self.image_orig = self.image_flipped
        else:
            self.image_orig = self.image_unflipped
            
        mouse_offset = self.mouse_pos - self.pivot
        mouse_angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        
        self.image, self.rect = self.rotate_on_pivot(self.image_orig, mouse_angle, self.pivot, self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def rotate_on_pivot(self, image, angle, pivot, origin):
        surf = pygame.transform.rotate(image, angle)
        
        offset = pivot + (origin - pivot).rotate(-angle)
        rect = surf.get_rect(center = offset)
        
        return surf, rect
    
    def handle_image_change_by_mouse_pos(self, pivot, mouse_pos):
        self.pivot = pivot
        
        distance = mouse_pos.distance_to(Vector2(self.pivot))

        self.x_scale = int(distance)
        self.x_pos_increment = int(distance / 2)

        self.image_orig = pygame.transform.scale(self.laser, (self.x_scale, 20))
        self.image = self.image_orig
        self.image_unflipped = pygame.transform.scale(self.laser, (self.x_scale, 20))
        self.image_flipped = pygame.transform.flip(self.image_orig, False, True)

        self.pos = Vector2(self.pivot) + (self.x_pos_increment, 0)
        self.rect = self.image.get_rect(center = self.pos)