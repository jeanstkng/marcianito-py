import os
import pygame
import random, uuid

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game_state):
        super().__init__()
        self.id = uuid.uuid4()
        self.image = pygame.image.load(os.path.join('images','asteroid.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 1280), random.randint(0, 720))
        self.game_state = game_state
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        is_over_asteroid = self.rect.collidepoint(pygame.mouse.get_pos())
                
        if is_over_asteroid:
            self.game_state.over_asteroid_id = self.id
            self.game_state.is_over_asteroid = True
            if self.game_state.laser_reached:
                self.image = self.create_image_surface_with_fog(self.image,(255, 0, 0), 0.005)
        elif self.game_state.over_asteroid_id == self.id and not is_over_asteroid:
            self.game_state.over_asteroid_id = ""
            self.game_state.is_over_asteroid = False
    
    def create_image_surface_with_fog(self, img, fog_color, fog_rate):
        _,_,w,h = img.get_rect()
        fog_color = [x*fog_rate for x in fog_color]
        new_surface = pygame.Surface((w,h), pygame.SRCALPHA, 32)
        new_surface.blit(img,img.get_rect())
        new_surface.fill((255,0,0, 100),img.get_rect(),special_flags=pygame.BLEND_MULT)
        new_surface.fill(fog_color,img.get_rect(),special_flags=pygame.BLEND_RGB_ADD)
        return new_surface