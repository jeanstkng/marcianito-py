from pygame import Vector2
from constants import game_constants

class GameState():
    def __init__(self):
        self.worldSize = Vector2(game_constants.get("window_width"), game_constants.get("window_height"))
        self.playerPos = Vector2(self.worldSize.x / 2, self.worldSize.y / 2)

    def update(self, moveTo):
        self.playerPos += moveTo
        
        if self.playerPos.x < 0:
            self.playerPos.x = 0
        elif self.playerPos.x >= self.worldSize.x:
            self.playerPos.x = self.worldSize.x - 1
            
        if self.playerPos.y < 0:
            self.playerPos.y = 0
        elif self.playerPos.y >= self.worldSize.y:
            self.playerPos.y = self.worldSize.y - 1