import os

import pygame, pygame_gui
from pygame.locals import *
from pygame.math import Vector2
from player import Player
from constants import game_constants
from background import Background
from laser_beam import LaserBeam
from asteroid import Asteroid
from game_state import GameState
from enemy import Enemy

os.environ["SLD_VIDEO_CENTERED"] = "1"

screen_size = Vector2(game_constants.get("window_width"), game_constants.get("window_height"))
screen_center = screen_size // 2
class Game():
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption("Marcianito 100% Real")
        game_icon = pygame.image.load(os.path.join('data','images','icon.png'))
        pygame.display.set_icon(game_icon)
        
        pygame.mixer.music.load(os.path.join('data','sounds','cumbia.mp3'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)
        
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        
        self.surface = pygame.display.set_mode((game_constants.get("window_width"),
                                               game_constants.get("window_height")))
        
        self.gui_manager = pygame_gui.UIManager((game_constants.get("window_width"),
                                               game_constants.get("window_height")), "theme.json")
        
        self.running = True
        self.gui_main_menu_manager = pygame_gui.UIManager((game_constants.get("window_width"),
                                               game_constants.get("window_height")), "theme.json")
        self.is_main_menu = True
        
        self.instance_game()
        
        self.health_bar = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((24, 24), (256, 24)),
                                                                manager=self.gui_manager, sprite_to_monitor=self.player)
        self.text_score = pygame_gui.elements.UILabel(text="0", relative_rect=pygame.Rect((1000, 6), (280, 64)), manager=self.gui_manager)

        self.text_timer = pygame_gui.elements.UILabel(text="03:00", relative_rect=pygame.Rect((600, 6), (100, 64)), manager=self.gui_manager)
        
        self.bg_main_menu = pygame.image.load(os.path.join('data','images','main_menu.png')).convert()
        self.button_play = pygame_gui.elements.UIButton(text="PLAY", relative_rect=pygame.Rect((540, 300), (200, 86)), manager=self.gui_main_menu_manager)
        self.button_exit = pygame_gui.elements.UIButton(text="EXIT", relative_rect=pygame.Rect((540, 400), (200, 86)), manager=self.gui_main_menu_manager)

        self.is_game_over = False
        self.text_final_score = pygame_gui.elements.UILabel(text="FINAL SCORE: 0", relative_rect=pygame.Rect((380, 300), (500, 86)), manager=self.gui_main_menu_manager)
        self.button_main_menu = pygame_gui.elements.UIButton(text="MAIN MENU", relative_rect=pygame.Rect((380, 400), (500, 86)), manager=self.gui_main_menu_manager)
        self.text_final_score.visible = 0
        self.button_main_menu.visible = 0

    def processInput(self):
        if self.is_main_menu or self.is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif (event.type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.button_exit):
                    self.running = False
                    break
                elif (event.type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.button_play):
                        self.is_main_menu = False
                        self.button_exit.visible = 0
                        self.button_play.visible = 0
                elif (event.type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.button_main_menu):
                    self.is_main_menu = True
                    self.is_game_over = False
                    self.instance_game()
                    self.game_state.init_state()
                    self.button_exit.visible = 1
                    self.button_play.visible = 1
                    self.button_main_menu.visible = 0
                    self.text_final_score.visible = 0
                    self.health_bar.set_sprite_to_monitor(self.player)
                self.gui_main_menu_manager.process_events(event)
                    
            return

        self.movement = Vector2(0,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.game_state.laser_attack_increment = 20
            self.gui_manager.process_events(event)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.movement.x = 12
        elif keys[pygame.K_a]:
            self.movement.x = -12
        elif keys[pygame.K_s]:
            self.movement.y = 12
        elif keys[pygame.K_w]:
            self.movement.y = -12
    
    def update(self):
        if self.is_main_menu or self.is_game_over:
            self.gui_main_menu_manager.update(self.delta_time)
            return
        
        if self.game_state.player_health < 1 or self.timer <= 0:
            self.is_game_over = True
            self.text_final_score.set_text("FINAL SCORE: " + str(self.game_state.score + (len(self.game_state.followers) * 100)))
            self.button_main_menu.visible = 1
            self.text_final_score.visible = 1
            return 
        
        self.player.update(self.movement)
        self.laser_beam.update(self.player.rect.center)
        self.bg.update(self.player.rect)
        self.targets[:] = [target for target in self.targets if target.is_alive]
        
        if len(self.targets) <= 10:
            self.targets.extend([Asteroid(self.game_state, False) for _ in range(10)])
        
        if len(self.enemies) <= 4:
            self.enemies.extend([Enemy(self.game_state) for _ in range(4)])
        
        for target in self.targets:
            target.update(self.clock.get_time())
        
        for enemy in self.enemies:
            enemy.update(self.clock.get_time())
            x_enemy = enemy.rect.center[0]
            if x_enemy > 0 and x_enemy < 1280:
                enemy.laser_beam.update(enemy.rect.center)
            else:
                enemy.laser_beam.reset_image_change()
        
        for follower in self.game_state.followers:
            follower.update(self.delta_time, self.player.rect.center)
            
        self.gui_manager.update(self.delta_time)

        if self.timer > 0:
            self.timer -= self.clock.get_time()
        else:
            self.timer = 0
        
        self.text_timer.set_text(self.milliseconds_to_minutes(self.timer))
        self.text_score.set_text(str(self.game_state.score))

    def render(self):
        self.surface.fill((0,0,0))
        
        if self.is_main_menu:
            self.surface.blit(self.bg_main_menu, (0, 0))
            self.gui_main_menu_manager.draw_ui(self.surface)
            pygame.display.flip()
            return
        
        self.bg.draw()
        self.laser_beam.draw(self.surface)
        
        for follower in self.game_state.followers:
            if not follower.is_rendered:
                self.all_sprites.add(follower)
                follower.is_rendered = True
            follower.animate()
            
        for target in self.targets:
            if not target.is_rendered:
                self.all_sprites.add(target)
                target.is_rendered = True
                
        for enemy in self.enemies:
            enemy.laser_beam.draw(self.surface)
            
        self.player.animate()
        self.all_sprites.draw(self.surface)
        
        self.gui_manager.draw_ui(self.surface)
        
        if self.is_game_over:
            self.gui_main_menu_manager.draw_ui(self.surface)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.delta_time = self.clock.tick(60) / 1000.0
            
    def instance_game(self):
        self.timer = 180000
        self.movement = pygame.Vector2(0,0)
        self.game_state = GameState()
        self.bg = Background(self.surface, self.game_state)
        self.player = Player(self.game_state)
        self.targets = [Asteroid(self.game_state) for _ in range(20)]
        self.enemies = [Enemy(self.game_state) for _ in range(8)]
        self.all_sprites = pygame.sprite.Group(self.player, self.targets, self.enemies)
        self.laser_beam = LaserBeam(self.player.rect.center, self.game_state)
            
    def seconds_to_minutes(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return '{:02d}:{:02d}'.format(minutes, seconds)

    def milliseconds_to_minutes(self, milliseconds):
        seconds = milliseconds // 1000
        return self.seconds_to_minutes(seconds)

game = Game()
game.run()
pygame.quit()