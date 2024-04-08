import pygame
from game_state import game_constants

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.frame_width = 96
        self.frame_height = 128
        self.frames_per_row = 5
        self.total_frames = 77
        self.rows, self.cols = self.calculate_layout()
        self.current_frame = 0
        self.image = self.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.topleft = (640, 360)  # Initial position
        self.speed = 5
        self.screen_width = game_constants.get("window_width")
        self.screen_height = game_constants.get("window_height")

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

    def update(self, movement):
        self.rect.move_ip(movement.x, movement.y)
        # Clamp to screen bounds if needed
        self.rect.left = max(0, min(self.rect.left, self.screen_width - self.rect.width))
        print(self.rect.left)
        self.rect.top = max(0, min(self.rect.top, self.screen_height - self.rect.height))

    def animate(self):
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.image = self.get_current_frame()
