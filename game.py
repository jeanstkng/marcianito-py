# import os
# import pygame
# from pygame import Vector2, Rect
# from game_state import GameState
# from constants import game_constants

# os.environ["SLD_VIDEO_CENTERED"] = "1"

# class Game():
#     def __init__(self):
#         pygame.init()
        
#         self.gameState = GameState()
        
#         self.window = pygame.display.set_mode((game_constants.get("window_width"),
#                                                game_constants.get("window_height")))
        
#         self.cellSize = Vector2(96, 128)
#         self.playerSprite = pygame.image.load("marcianito.png")
        
#         pygame.display.set_caption("Marcianito 100% Real")
#         self.clock = pygame.time.Clock()
#         self.running = True
#         self.movement = pygame.Vector2(0,0)

#     def processInput(self):
#         self.movement = Vector2(0,0)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#                 break
        
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_ESCAPE]:
#             self.running = False
#         elif keys[pygame.K_d]:
#             self.movement.x = 8
#         elif keys[pygame.K_a]:
#             self.movement.x = -8
#         elif keys[pygame.K_s]:
#             self.movement.y = 8
#         elif keys[pygame.K_w]:
#             self.movement.y = -8
    
#     def update(self):
#         self.gameState.update(self.movement)

#     def render(self):
#         self.window.fill((0,0,0))
        
#         spritePoint = self.gameState.playerPos.elementwise() * self.cellSize
#         texturePoint = Vector2(1,0).elementwise() * self.cellSize
#         textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
#         self.window.blit(self.playerSprite, spritePoint, textureRect)
        
#         pygame.display.update()
    
#     def run(self):
#         while self.running:
#             self.processInput()
#             self.update()
#             self.render()
#             self.clock.tick(60)
        
# game = Game()
# game.run()
# pygame.quit()
import pygame
from pygame.locals import *
from pygame.math import Vector2

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
        self.rect.topleft = (100, 100)  # Initial position
        self.velocity = Vector2(0, 0)
        self.speed = 5

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

    def update(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        # Clamp to screen bounds if needed
        self.rect.left = max(0, min(self.rect.left, screen_width - self.rect.width))
        self.rect.top = max(0, min(self.rect.top, screen_height - self.rect.height))

    def animate(self):
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.image = self.get_current_frame()

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

sprite_sheet = pygame.image.load("marcianito.png")

player = Player(sprite_sheet)
all_sprites = pygame.sprite.Group(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.velocity = Vector2(0, 0)
    if keys[K_LEFT]:
        player.velocity.x = -player.speed
    if keys[K_RIGHT]:
        player.velocity.x = player.speed
    if keys[K_UP]:
        player.velocity.y = -player.speed
    if keys[K_DOWN]:
        player.velocity.y = player.speed

    all_sprites.update()
    player.animate()

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(10)  # Adjust the frame rate as needed

pygame.quit()
