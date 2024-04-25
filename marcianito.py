import pygame
import math
from constants import game_constants

class Marcianito(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, scale = False):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.frame_width = 96
        self.frame_height = 128
        self.frames_per_row = 5
        self.total_frames = 77
        self.rows, self.cols = self.calculate_layout()
        self.current_frame = 0
        self.image = pygame.transform.scale(self.get_current_frame(), (scale, scale)) if scale else self.get_current_frame()
        self.scale = scale
        self.rect = self.image.get_rect()
        self.rect.topleft = (640, 360)
        self.screen_width = game_constants.get("window_width")
        self.screen_height = game_constants.get("window_height")
        self.speed = 400
        self.target_pos = (0, 0)
        
    def calculate_layout(self):
        rows = self.total_frames // self.frames_per_row
        cols = self.frames_per_row
        if self.total_frames % self.frames_per_row != 0:
            rows += 1
            cols = self.total_frames % self.frames_per_row
        return rows, cols

    def get_current_frame(self):
        row = self.current_frame // self.frames_per_row
        col = self.current_frame % self.frames_per_row if row < self.rows - 1 else self.current_frame % self.cols
        frame_rect = pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
        frame_image = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame_image.blit(self.sprite_sheet, (0, 0), frame_rect)
        return frame_image

    def update(self, dt, player_pos):
        modified_player_x = player_pos[0] + 100
        if player_pos[0] > self.screen_width / 2:
            modified_player_x = player_pos[0] - 100
        
        self.target_pos = (modified_player_x, player_pos[1] + 24)
        
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist > self.speed * dt:
            angle = math.atan2(dy, dx)
            move_distance = self.speed * dt
            self.rect.move_ip(move_distance * math.cos(angle), move_distance * math.sin(angle))
        else:
            self.rect.center = self.target_pos

    def animate(self):
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.image = pygame.transform.scale(self.get_current_frame(), (self.scale, self.scale)) if self.scale else self.get_current_frame()
